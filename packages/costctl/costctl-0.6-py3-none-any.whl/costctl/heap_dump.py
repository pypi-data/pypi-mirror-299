from kubernetes import client, config
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException
import os
import sys
from inquirer import List
import io
import subprocess
from datetime import timedelta

kubeconfig_path = os.getenv('KUBECONFIG')

def upload_to_minio(minioHost, minio_access_key, minio_secret_key, bucketName, objectName, local_dump_path):
    try:
        minio_client = Minio(minioHost,
                             access_key=minio_access_key,
                             secret_key=minio_secret_key,
                             secure=False)  # Change to True if you're using HTTPS

        if not minio_client.bucket_exists(bucketName):
            minio_client.make_bucket(bucketName)

        minio_client.fput_object(bucketName, objectName, local_dump_path)
        print(f"File uploaded to Minio bucket: {bucketName}/{objectName}")
    except S3Error as e:
        print(f"Error uploading file to Minio: {e}")

def generateMinioPresignedUrl(minioHost, minio_access_key, minio_secret_key, bucketName, objectName, expires=timedelta(hours=2)):
    try:
        minio_client = Minio(minioHost,
                             access_key=minio_access_key,
                             secret_key=minio_secret_key,
                             secure=False)  # Change to True if you're using HTTPS

        # Generate a pre-signed URL for the object
        url = minio_client.presigned_get_object(bucketName, objectName, expires=expires)
        print(url)
        return url
    except S3Error as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

def list_pids_in_pod(namespace, pod_name, api_instance):
    config.load_kube_config(config_file=kubeconfig_path)
    exec_command=["sh","-c","ps -ef"]
    api_instance = client.CoreV1Api()

    try:
        resp = stream(api_instance.connect_get_namespaced_pod_exec, pod_name, namespace, command=exec_command, stderr=True, stdin=False, stdout=True, tty=False,container="app")
        print(resp)
        return resp
    except ApiException as e:
        print(f"Error listing PIDs in the pod: {e}")
        sys.exit(1)

def get_selected_pid(pid_values,command_values):
    print("Select a PID to capture a heap dump:")
    count = 0
    for pid, command in zip(pid_values, command_values):
        count += 1
        print(f"{count}. {pid} - {command}")
    # for i, pid in enumerate(pids, 1):
    #     print(f"{i}. {pid}")

    while True:
        try:
            choice = int(input("Enter the number of the PID: "))
            if 1 <= choice <= len(pid_values):
                selected_pid = pid_values[choice - 1]
                return selected_pid
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def pod_exec(pod_name, namespace, exec_command, api_instance):

    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False,
                  _preload_content=False,container="app")

    while resp.is_open():
        resp.update(timeout=6)
        if resp.peek_stdout():
            print(f"STDOUT: \n{resp.read_stdout()}")
        if resp.peek_stderr():
            print(f"STDERR: \n{resp.read_stderr()}")

    resp.close()

    if resp.returncode != 0:
        raise Exception("Script failed")

def copy_heap_dump(namespace, pod_name, local_dump_path):
    config.load_kube_config(config_file=kubeconfig_path)
    
    try:
        # Build the kubectl cp command
        container_path = '/tmp/heap_dump.hprof'
        command = [
            'kubectl', 'cp',
            f'{namespace}/{pod_name}:{container_path}', 
            local_dump_path,
            '--kubeconfig', 'files/kubeconfig.yaml'
        ]
        
        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"File copied from pod to {local_dump_path}")
        else:
            print(f"Error copying file: {result.stderr.decode('utf-8')}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error copying file: {e.stderr.decode('utf-8')}")

# Example usage
 
def generateHeapOrThreadDump(pod_name,namespace,api_instance,local_dump_path,heapDump):
    print("Listing available PIDs in the pod:")
    pids = []
    data = list_pids_in_pod(namespace, pod_name, api_instance)
    lines = data.strip().split('\n')

    # Extract headers
    headers = lines[0].split()

    # Initialize an empty dictionary
    pid_values = []
    command_values = []

    # Iterate over the lines and populate the lists
    for line in lines[1:]:
        values = line.split()
        pid_values.append(values[0])
        command_values.append(' '.join(values[3:]))
    ############ GET PID ID's #################
    # print(pids)
    # process = []
    # for line in ps_output.split('\n'):
    #     print(line)
    #     if line.strip() and not line.startswith("PID"):
    #         parts = line.split()
    #         if len(parts) > 1:
    #             pids.append(parts[0])
    # print(pids)
    # if not pids:
    #     print("No PIDs found in the pod. Make sure the pod is running Java processes.")
    #     sys.exit(1)

    #user to select a PID from the list
    selected_pid = get_selected_pid(pid_values,command_values)
    print(selected_pid)

    if(heapDump == True):
        try:
            api_instance = client.CoreV1Api()
            exec_command = ["sh", "-c", f"jcmd {selected_pid} GC.heap_dump -all /tmp/heap_dump.hprof"]
            resp = pod_exec(pod_name,namespace,exec_command,api_instance)
            print(resp)
            copy_heap_dump(namespace, pod_name, local_dump_path)
        except ApiException as e:
            print(f"Failed to take a heap dump using jcmd. Trying with jmap: {e}")
            # If jcmd fails, try using jmap
            # try:
            #     exec_command = ["/bin/sh", "-c", f"jmap -dump:format=b,file=/tmp/heap_dump.hprof {selected_pid}"]
            #     resp = pod_exec(pod_name,namespace,exec_command,api_instance)
            #     print(resp)
            # except ApiException as e:
            #     print(f"Error while executing jmap command: {e}")
            #     sys.exit(1)
            #     return

        # copy_heap_dump(namespace, pod_name, local_dump_path, api_instance)
    else:
        try:
            api_instance = client.CoreV1Api()
            exec_command = ["sh", "-c", f"jcmd {selected_pid} Thread.print /tmp/thread_dump.hprof"]
            resp = pod_exec(pod_name,namespace,exec_command,api_instance)
            print(resp)
        except ApiException as e:
            print(f"Failed to take a heap dump using jcmd. Trying with jmap: {e}")

            # If jcmd fails, try using jmap
            try:
                exec_command = ["sh", "-c", f"kill -3 {selected_pid}"]
                resp = pod_exec(pod_name,namespace,exec_command,api_instance)
                print(resp)
            except ApiException as e:
                print(f"Error while executing jmap command: {e}")
                sys.exit(1)
                return

        copy_heap_dump(namespace, pod_name, local_dump_path)

def main():
    config.load_kube_config(config_file=kubeconfig_path)
    api_instance = client.CoreV1Api()
    ######## fix hard coded at later date #########
    namespace = input("Enter the namespace: ")
    pod_name = input("Enter the pod name: ")
    user_id = input("Enter your Lowes Sales ID: ")
    local_dump_path = "/Users/"+user_id+"/Documents/"+pod_name+".hprof"
    objectName = pod_name+"heapDump" 
    heapDump = True
    generateHeapOrThreadDump(pod_name,namespace,api_instance,local_dump_path,heapDump)
    # copy_heap_dump(namespace,pod_name, local_dump_path)
    # upload_to_minio(minioHost, minio_access_key, minio_secret_key, bucketName, objectName, local_dump_path)
    # generateMinioPresignedUrl(minioHost, minio_access_key, minio_secret_key, bucketName, objectName, expires=timedelta(hours=2))

if __name__ == "__main__":
    main()