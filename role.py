import sys
import boto3
import botocore


def get_args():
	if len(sys.argv) != 3:
		error_message = 'Please supply a total of 2 arguments to this script: AccountID, roleName'
		sys.exit(error_message)
	else:
		ACCOUNTID=sys.argv[1]
		ROLENAME=sys.argv[2]
		return {
		    'account_id': ACCOUNTID,
		    'rolename': ROLENAME
		}

def assume_role(account_id, rolename):
    AccepterRoleArn = 'arn:aws-us-gov:iam::{account_id}:role/{rolename}'.format(account_id=account_id,rolename=rolename)
    
    try: 
        response = sts_client.assume_role(
		    RoleArn=AccepterRoleArn,
		    RoleSessionName='RoleToAuthorizeRoleCreation',
		    DurationSeconds=900		)
        
        access_key=response['Credentials']['AccessKeyId']
        secret_key=response['Credentials']['SecretAccessKey']
        token=response['Credentials']['SessionToken']

	return boto3.Session(
	    aws_access_key_id=access_key,
	    aws_secret_access_key=secret_key,
	    aws_session_token=token
	)
    except botocore.exceptions.ClientError as e:
        raise e


if __name__=='__main__':
    args = get_args()
    sts_client = boto3.client('sts')
    account_id = args['account_id']
    rolename = args['rolename']

    assume_role(account_id, rolename)

