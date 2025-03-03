resource "aws_key_pair" "chatqna_key" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.ssh_public_key_path)
}

resource "aws_instance" "chatqna" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [var.security_group_id]
  key_name               = aws_key_pair.chatqna_key.key_name

  root_block_device {
    volume_size = var.root_volume_size
    volume_type = "gp3"
  }

  user_data = templatefile("${path.module}/userdata.tftpl", {
    huggingface_token    = var.huggingface_token
    opea_release_version = var.opea_release_version
  })

  tags = {
    Name = "${var.project_name}-instance"
  }

  provisioner "local-exec" {
    command = templatefile("${path.module}/${var.host_os}-ssh-config.tpl", {
      hostname     = self.public_ip,
      user         = "ubuntu",
      identityfile = "~/.ssh/id_opea_docsum"
    })
    interpreter = var.host_os == "windows" ? ["Powershell", "-Command"] : ["bash", "-c"]
  }
}

# Create a local file with the rendered SSH config (Linux)
resource "local_file" "ssh_config_linux" {
  content = templatefile("${path.module}/linux-ssh-config.tpl", {
    hostname     = aws_instance.chatqna.public_ip
    user         = "ubuntu"
    identityfile = var.ssh_private_key_path
  })
  filename = "${path.cwd}/ssh_config_${var.project_name}.txt"
}
