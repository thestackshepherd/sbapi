terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # This config has no remote backend by design — it creates the
  # bucket/table that the main config's remote backend depends on.
}
