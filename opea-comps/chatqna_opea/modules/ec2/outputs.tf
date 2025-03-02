output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.chatqna.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.chatqna.public_ip
}

output "public_dns" {
  description = "Public DNS name of the EC2 instance"
  value       = aws_instance.chatqna.public_dns
}

output "ssh_key_name" {
  description = "Name of the SSH key pair used for the instance"
  value       = aws_key_pair.chatqna_key.key_name
}

output "ssh_config_file" {
  description = "Path to the generated SSH config file"
  value       = local_file.ssh_config_linux.filename
} 