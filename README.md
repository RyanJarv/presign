# presign

A simple script around boto3 that prints pre-signed AWS requests for any service.

## Examples

```bash
python3 ./main.py --profile test-a sts assume-role RoleArn arn:aws:iam::123456789012:role/test RoleSessionName test
```
