ui = true

storage "file" {
  path = "/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "/vault/ssl/domain.crt"
  tls_key_file = "/vault/ssl/domain.key"
}

disable_mlock = true

api_addr = "https://0.0.0.0:8200"
cluster_addr = "https://0.0.0.0:8201"

default_lease_ttl = "168h"
max_lease_ttl = "720h"
