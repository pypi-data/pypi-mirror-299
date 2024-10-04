import socket
import json
import hashlib
from datetime import datetime

def synapse(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"synapse connected to {ip}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        try:
            # Receive data from the client
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            # Deserialize JSON data
            json_data = json.loads(data)

            # Prepare a response
            response = {"status": "success", "received": json_data}
            response_data = json.dumps(response)

            # Send response back to client
            conn.sendall(response_data.encode('utf-8'))
        except json.JSONDecodeError:
            print("Failed to decode JSON")
        finally:
            # Close the connection
            conn.close()


def nt(ip, port, transmitter):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transmitter_id = hashlib.sha1(f"{transmitter}{timestamp}".encode()).hexdigest()
    transmit = {
        "id": transmitter_id,
        "transmitter": transmitter
    }
    
    try:
        # Create a socket and connect to the node
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))
        print(f"Connected to {ip}:{port}")

        # Send JSON data
        json_slice = json.dumps(transmit)  # Convert transmit dictionary to JSON
        client_socket.sendall(json_slice.encode('utf-8'))
        print(f"Sent data to {ip}:{port}")

        # Receive response
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Received response from {ip}:{port}: {response}")

    except Exception as e:
        print(f"Failed to connect to {ip}:{port}: {e}")

    finally:
        client_socket.close()


def circuit(cells, transmitter):
    for cell in cells:
        address = cell["address"]
        ip, port = address.split(":")
        port = int(port)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transmitter_id = hashlib.sha1(f"{transmitter}{timestamp}".encode()).hexdigest()
        transmit = {
            "id": transmitter_id,
            "transmitter": transmitter
        }
        
        try:
            # Create a socket and connect to the node
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            print(f"Connected to {ip}:{port}")

            # Send JSON data
            json_slice = json.dumps(transmit)  # Convert transmit dictionary to JSON
            client_socket.sendall(json_slice.encode('utf-8'))
            print(f"Sent data to {ip}:{port}")

            # Receive response
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Received response from {ip}:{port}: {response}")

        except Exception as e:
            print(f"Failed to connect to {ip}:{port}: {e}")

        finally:
            client_socket.close()




