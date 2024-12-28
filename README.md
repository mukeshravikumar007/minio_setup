# MinIO Setup

## Overview

### MinIO Server
MinIO Server is a high-performance object storage server designed for unstructured data storage. It supports the Amazon S3 API, making it compatible with various applications and tools. MinIO Server is ideal for building scalable and reliable storage solutions for cloud-native applications.

### MinIO Client (mc)
The MinIO Client (mc) is a command-line tool that simplifies management and interaction with MinIO deployments. It provides functionalities such as bucket management, file uploads, downloads, and synchronization across multiple nodes, making it a versatile tool for administrators.

### MinIO SDK
MinIO SDKs are available in multiple programming languages (e.g., Python, Java, Go, and JavaScript), enabling developers to integrate MinIO storage into their applications seamlessly. These SDKs provide APIs for object storage operations, including file uploads, downloads, and bucket management, making it easier to build custom solutions on top of MinIO.

This guide provides step-by-step instructions for setting up MinIO in both single-node and multi-node configurations. MinIO is a high-performance object storage system that is compatible with Amazon S3 APIs.

## Prerequisites

- **Operating System**: Linux (e.g., Ubuntu 24.04)
- **Dependencies**:
  - wget
  - tar
  - systemctl (for service management)
- **Network**: Ensure nodes can communicate over the required ports.

## Single-Node Configuration

### Step 1: Download and Install MinIO
1. Download the MinIO server binary:
   ```bash
   wget https://dl.min.io/server/minio/releases/linux-amd64/minio
   chmod +x minio
   sudo mv minio /usr/local/bin/
   ```

2. Create a directory for data storage:
   ```bash
   sudo mkdir -p /mnt/minio-data
   sudo chown -R $USER:$USER /mnt/minio-data
   ```

### Step 2: Start MinIO Server
Run the MinIO server with the following command:
```bash
minio server /mnt/minio-data --console-address ":9001"
```

### Step 3: Access the MinIO Console
- Open a browser and navigate to `http://<your-server-ip>:9001`
- Log in with the default credentials:
  - **Username**: `minioadmin`
  - **Password**: `minioadmin`

### Step 4: Configure MinIO as a Service (Optional)
To run MinIO as a systemd service:
1. Create a service file:
   ```bash
   sudo nano /etc/systemd/system/minio.service
   ```
2. Add the following content:
   ```ini
   [Unit]
   Description=MinIO Object Storage
   After=network.target

   [Service]
   User=<your-username>
   Group=<your-group>
   ExecStart=/usr/local/bin/minio server /mnt/minio-data --console-address ":9001"
   Restart=always
   RestartSec=10s

   [Install]
   WantedBy=multi-user.target
   ```
3. Reload systemd and enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable minio
   sudo systemctl start minio
   ```

### Single-Node with 2 Disks
1. **Prepare the Disks**: 
   - Ensure both disks are mounted (e.g., `/mnt/disk1` and `/mnt/disk2`).
   - Set permissions to allow MinIO access:
     ```bash
     sudo chown -R $USER:$USER /mnt/disk1 /mnt/disk2
     ```

2. **Start MinIO Server**:
   - Launch the MinIO server with both disks:
     ```bash
     minio server /mnt/disk1 /mnt/disk2 --console-address ":9001"
     ```

## Multi-Node Configuration

### Step 1: Install MinIO on Each Node
Repeat the installation steps from the Single-Node Configuration on each node.

### Step 2: Configure Distributed MinIO
1. Ensure each node has a directory for data storage (e.g., `/mnt/minio-data`).
2. Start the MinIO server in distributed mode:
   ```bash
   minio server http://node1-address:9000/mnt/minio-data http://node2-address:9000/mnt/minio-data
   ```
   Replace `node1-address` and `node2-address` with the IP addresses or hostnames of the nodes.

### Multi-Node with 2 Disks
1. **Prepare the Disks on Each Node**:
   - Repeat the steps to prepare two disks on each node, ensuring unique mount points (e.g., `/mnt/disk1` and `/mnt/disk2`).

2. **Start Distributed MinIO**:
   - Configure distributed MinIO using all disks across both nodes:
     ```bash
     minio server http://node1-address:9000/mnt/disk1 http://node1-address:9000/mnt/disk2 \
                  http://node2-address:9000/mnt/disk1 http://node2-address:9000/mnt/disk2
     ```

### Step 3: Access the MinIO Console
- Use the same steps as in the single-node setup to access the console.

### Step 4: Verify the Setup
- Check the status of the distributed setup using the MinIO console or the CLI.

## MinIO Client (mc) Setup

The MinIO Client (mc) provides a command-line tool to manage your MinIO deployments and interact with object storage systems.

### Step 1: Download and Install mc
1. Download the MinIO Client binary:
   ```bash
   wget https://dl.min.io/client/mc/release/linux-amd64/mc
   chmod +x mc
   sudo mv mc /usr/local/bin/
   ```

### Step 2: Configure mc for Single Node
1. Add a new alias for your MinIO server:
   ```bash
   mc alias set myminio http://<your-server-ip>:9000 <access-key> <secret-key>
   ```
   Replace `<your-server-ip>`, `<access-key>`, and `<secret-key>` with your server's details.

2. Test the connection:
   ```bash
   mc ls myminio
   ```

### Step 3: Configure mc for Multi-Node
1. Add aliases for both nodes:
   ```bash
   mc alias set node1 http://node1-address:9000 <access-key> <secret-key>
   mc alias set node2 http://node2-address:9000 <access-key> <secret-key>
   ```
   Replace `node1-address` and `node2-address` with the IP addresses or hostnames of the nodes.

2. Verify connections for both nodes:
   ```bash
   mc ls node1
   mc ls node2
   ```

3. Synchronize buckets or data between nodes:
   ```bash
   mc mirror node1/mybucket node2/mybucket
   ```

### Step 4: Common Commands
- **List buckets**:
  ```bash
  mc ls myminio
  ```
- **Create a bucket**:
  ```bash
  mc mb myminio/mybucket
  ```
- **Upload a file**:
  ```bash
  mc cp /path/to/file myminio/mybucket
  ```
- **Download a file**:
  ```bash
  mc cp myminio/mybucket/file /path/to/destination
  ```
- **Remove a file or bucket**:
  ```bash
  mc rm myminio/mybucket/file
  mc rb myminio/mybucket
  ```

### Step 5: Advanced Configuration
- **Mirror Directories**:
  Sync local and remote directories:
  ```bash
  mc mirror /local/path myminio/mybucket
  ```

- **Set Policies**:
  Manage bucket policies (e.g., make a bucket public):
  ```bash
  mc policy set public myminio/mybucket
  ```

## Additional Configuration
- **Environment Variables**:
  Set access and secret keys in `/etc/default/minio`:
  ```bash
  export MINIO_ROOT_USER=<your-access-key>
  export MINIO_ROOT_PASSWORD=<your-secret-key>
  ```

- **TLS Configuration**:
  For secure connections, generate TLS certificates and place them in the `~/.minio/certs` directory.

## Troubleshooting
- **Ports**: Ensure ports (9000, 9001) are open and accessible.
- **Logs**: Check logs with:
  ```bash
  sudo journalctl -u minio
  ```

## References
- [MinIO Documentation](https://min.io/docs)
- [MinIO GitHub Repository](https://github.com/minio/minio)

---
Happy hosting with MinIO! 🚀
