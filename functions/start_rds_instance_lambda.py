import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(rds, instancia):

    rds = boto3.client('rds')

    instancia = os.getenv('DBName')

    status = get_status(rds, instancia)

    logger.info(f"Status da instancia: {status}")

    if (status != "stopped"):
        logger.info("Start cancelado devido ao status diferente de 'stopped'")
        return {
            'start': False,
            'motivo': f'Status {status} diferente de stopped'
        }

    logger.info(f"Iniciando start RDS: {instancia}")
    response = rds.start_db_instance(DBInstanceIdentifier=instancia)
    logger.info(f"Start RDS bem sucedido: {response}")
    return {
        'start': True
    }


def get_status(rds, instancia):
    response = rds.describe_db_instances(DBInstanceIdentifier=instancia)
    return response['DBInstances'][0]['DBInstanceStatus']