group "default" {
  targets = ["app"]
}

target "app" {
  dockerfile = "Dockerfile"
  context = "."
  tags = ["docker.io/buechijonas/groceries-list:latest"]
}
