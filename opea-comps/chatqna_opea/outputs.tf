output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = module.ec2.public_ip
}

output "chatqna_url" {
  description = "URL to access the ChatQnA application"
  value       = "http://${module.ec2.public_ip}:80"
}

output "ssh_command" {
  description = "Command to SSH into the EC2 instance"
  value       = "ssh -i ${var.ssh_private_key_path} ubuntu@${module.ec2.public_ip}"
}

output "ssh_config_file" {
  description = "Path to the generated SSH config file"
  value       = module.ec2.ssh_config_file
}

output "ssh_config_instructions" {
  description = "Instructions for using the generated SSH config"
  value       = "To use the generated SSH config, run: cat ${module.ec2.ssh_config_file} | bash"
}

output "cloud_init_log" {
  description = "Command to check cloud-init logs on the instance"
  value       = "ssh -i ${var.ssh_private_key_path} ubuntu@${module.ec2.public_ip} 'sudo cat /var/log/cloud-init-output.log'"
} 