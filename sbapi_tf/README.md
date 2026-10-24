# infra

Terraform boilerplate for deploying sbapi to AWS as a container. ECR and the
actual compute (ECS/Lambda/etc.) are intentionally not defined yet — add
those to `main.tf` once the deployment target is decided.

## Layout

- `bootstrap/` — one-time setup, run standalone (no remote backend) to
  create the S3 bucket + DynamoDB table that the main config's state
  backend depends on.
- everything else — the main config, using the S3/DynamoDB backend created
  by `bootstrap/`.

## Usage

```sh
# 1. Create the state bucket + lock table (once, per AWS account)
cd bootstrap
terraform init
terraform apply

# 2. Configure the main config's backend
cd ..
cp backend.hcl.example backend.hcl   # fill in bucket/table names from step 1
terraform init -backend-config=backend.hcl
terraform apply
```
