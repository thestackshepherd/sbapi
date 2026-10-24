/*
  Remote state lives in S3 with DynamoDB locking.

  Terraform's backend block can't reference variables, so this stays empty
  and the real values are supplied at init time with a partial config:

    terraform init -backend-config=backend.hcl

  Copy backend.hcl.example to backend.hcl (gitignored) and fill it in, or
  run the bootstrap/ module first to create the bucket and lock table.
*/

terraform {
  backend "s3" {}
}
