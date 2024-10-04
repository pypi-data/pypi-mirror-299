import argparse
import os
import re
import subprocess
import time
from kubernetes import client, config
import kubernetes
from kubernetes.stream import stream
from kubernetes.client.rest import ApiException
from urllib3.exceptions import MaxRetryError

ENVIRONMENT = os.getenv('ENVIRONMENT')
kubeconfig_path = os.getenv('KUBECONFIG')

def get_pods_in_batches(api_instance, namespace=None, field_selector=None, batch_size=100, delay=0.1):
    continue_token = None
    while True:
        if namespace:
            pods = api_instance.list_namespaced_pod(namespace, field_selector=field_selector, limit=batch_size, _continue=continue_token)
        else:
            pods = api_instance.list_pod_for_all_namespaces(field_selector=field_selector, limit=batch_size, _continue=continue_token)
        
        yield from pods.items
        
        continue_token = pods.metadata._continue
        if not continue_token:
            break
        
        time.sleep(delay)

def dedup_file(filepath):
    filename, extension = os.path.splitext(filepath)
    with open(filepath, 'r') as f:
        lines = f.readlines()
    lines = [line for line in lines if not line.lstrip().startswith('#')]
    lines = sorted(set(lines))
    with open(f"{filename}-dedup{extension}", 'w') as f:
        f.writelines(lines)
    os.rename(f"{filename}-dedup{extension}", filepath)

def extract_replicaset(pod_name):
    return "-".join(pod_name.split("-")[:-2])
    
def contains(container, item):
    return "yes" if item in container.split() else "no"


def usage():
    print("Usage: script.py -d <directory>  [-n list of namespaces]")
    print("   use -n to limit search to set of namespaces")


def main(directory, namespaces):
    # parser = argparse.ArgumentParser(description='Process Kubernetes pods and get Java versions.')
    # parser.add_argument('-d', '--directory', required=True, help='Directory to store output files')
    # parser.add_argument('-n', '--namespaces', nargs='+', help='List of namespaces')

    # args = parser.parse_args()
    output_dir = directory
    namespaces = namespaces

    ignore_namespaces = "kube-external-secrets cattle-fleet-system logging-ns cattle-system gatekeeper-system kube-system keda istio-system kube-system webhooks wiz controllers telemetry-ns carbon-ltm-status test cleanup-operator prometheus-ns wiz twistlock-ns logging-ns goldpinger-ns cattle-systems carbon-test-app-ns carbon-health-ns carbon-genesis-ns cattle-system goldilocks-ns test"
    ignore_ns_list = ignore_namespaces.split()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(ENVIRONMENT)
    env = str(ENVIRONMENT)
    # Load the kubeconfig file from the current directory
    config.load_config(config_file=kubeconfig_path)
    v1 = client.CoreV1Api()

    all_pods_file = os.path.join(output_dir, "all.txt")

    with open(all_pods_file, 'w') as f:
        if namespaces:
            for namespace in namespaces:
                try:
                    for pod in get_pods_in_batches(v1, namespace=namespace, field_selector="status.phase=Running"):
                        images = " ".join([container.image for container in pod.spec.containers])
                        f.write(f"{pod.metadata.namespace} {pod.metadata.name} {images}\n")
                except ApiException as e:
                    print(f"Exception when calling CoreV1Api->list_namespaced_pod: {e}")
        else:
            try:
                for pod in get_pods_in_batches(v1, field_selector="status.phase=Running"):
                    images = " ".join([container.image for container in pod.spec.containers])
                    f.write(f"{pod.metadata.namespace} {pod.metadata.name} {images}\n")
            except ApiException as e:
                print(f"Exception when calling CoreV1Api->list_pod_for_all_namespaces: {e}")

    cleaned_file = os.path.join(output_dir, "cleaned.txt")
    with open(cleaned_file, 'w') as cleaned:
        with open(all_pods_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                ns, name, images = parts[0], parts[1], parts[2:]
                if contains(ignore_namespaces, ns) == "no":
                    for image in images:
                        if not re.search(r"(e-telem|ptp-docker-remote.docker.lowes.com/istio/proxyv2:1.17.5|registry-auth.twistlock.com)", image):
                            cleaned.write(f"{image} {ns} {name}\n")

    dedup_file(cleaned_file)

    versions_file = os.path.join(output_dir, "versions.csv")
    with open(versions_file, 'w') as versions:
        last_image = "none"
        last_output = "none"
        counter = 0

        with open(cleaned_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                image, ns, name = parts[0], parts[1], parts[2]

                if last_image != image:
                    try:
                        exec_command = [
                            '/bin/sh',
                            '-c',
                            'java --version || java -version'
                        ]
                        print(f"Executing command in pod {name} in namespace {ns}: {exec_command}")
                        output = stream(v1.connect_get_namespaced_pod_exec,
                                        name, ns,
                                        command=exec_command,
                                        stderr=True, stdin=False,
                                        stdout=True, tty=False,container="app")
                        print(f"Command output: {output}")
                        output = re.search(r"(openjdk.*?)(\r|\n|$)", output).group(1).strip() if output else "none"
                    except client.exceptions.ApiException as e:
                        print(f"ApiException when executing command in pod {name} in namespace {ns}: {e}")
                        output = "none"
                    except Exception as e:
                        print(f"Error executing command in pod {name} in namespace {ns}: {e}")
                        output = "none"
                    versions.write(f"{image},{ns},{name},{output}\n")
                    last_image = image
                    last_output = output
                else:
                    versions.write(f"{image},{ns},{name},{last_output}\n")

                counter += 1
                if counter == 300:
                    counter = 0
                    print("sleeping")
                    time.sleep(30)

    dedup_file(versions_file)

    def compare_versions(version1, version2):
        def version_to_tuple(version):
            version = version.replace("-ea", ".0")  # Replace `-ea` with `.0` for comparison
            return tuple(map(int, re.findall(r'\d+', version)))
    
        return version_to_tuple(version1) < version_to_tuple(version2)

    def check_string(input_string, regex, max_invalid):
        match = re.search(regex, input_string)
        if match:
            print(input_string)
            substring = match.group(0)
            print(compare_versions(substring, max_invalid))
            return compare_versions(substring, max_invalid)  # Ensure substring is strictly less than max_invalid
        return False

    bad_versions_file = os.path.join(output_dir, "bad_versions_java.csv")
    processed_replicasets = set()
    with open(bad_versions_file, 'w') as bad_versions:
        with open(versions_file, 'r') as versions:
            for line in versions:
                parts = line.strip().split(",")
                pod_name = parts[2]
                replicaset = extract_replicaset(pod_name)
                # cmdb = get_cmdb(namespace,podname)
                if replicaset in processed_replicasets:
                    continue
                
                if (check_string(line, r"1\.8\.0_[0-9]+", "1.8.0_372") or
                    check_string(line, r"11\.0\.[0-9]+", "11.0.16") or
                    check_string(line, r"1[2-6]\.[0-9]+\.[0-9]+|1[3-4]-ea", "17.0.0")):
                    bad_versions.write(line)
                    processed_replicasets.add(replicaset)

    bad_versions_count = sum(1 for _ in open(bad_versions_file)) if os.path.exists(bad_versions_file) else 0
    print(f"Completed, found {bad_versions_count} bad images")
    print(f"files are in {output_dir}")
    subprocess.run(['wc', '-l', os.path.join(output_dir, '*')])


if __name__ == '__main__':
    main()