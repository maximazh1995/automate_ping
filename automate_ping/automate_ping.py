from pythonping import ping
import time
import numpy
import click
import logging
import sys

logging.basicConfig(format='%(asctime)s - %(message)s', filename="automate_ping.log", level=logging.INFO)
logger = logging.getLogger()

def ping_server(target_ip, package_size, package_count):
    count_of_success_packages = 0
    try:
        response_list = ping(target_ip, size=package_size, count=package_count)
        for response in response_list:
            logger.info(response)
            if response.success:
                count_of_success_packages += 1
        return count_of_success_packages
    except Exception as Argument:
        logger.debug(Argument)


@click.command()
@click.argument('target_ip')
@click.argument('package_size')
def main(target_ip, package_size):
    """
    Скрипт для отправки icmp запросов на сервер: \n
        - количество попыток = 3 \n
        - количество icmp пакетов в одну попытку = 120 \n
        - интервал между попытками в секундах = 5 сек \n

    Обязательные аргументы: \n
        - target_ip: целевой адрес \n
        - package_size: размер пакета (без учета заголовка ICMP - 8 байт) \n
    """
    try:
        logger.info(f"Скрипт был запущен со следующими параметрами: целевой адрес: {target_ip} , размер пакета: {package_size}")

        # target_ip = '8.8.8.8'  # целевой адрес
        # package_size = 60  # размер пакета (без учета заголовка ICMP - 8 байт)
        package_count = 120  # количество icmp пакетов в одну попытку
        number_of_attempts = 3  # количество попыток
        success = [0] * number_of_attempts  # массив для хранения количества успешных попыток
        interval = 5  # интервал между попытками в секундах

        with click.progressbar(length=number_of_attempts, label=f'Running') as bar:
            for i in range(0, number_of_attempts):
                success[i] = ping_server(target_ip, int(package_size), package_count)
                logger.info(f"Задержка в {interval} секунд!")
                time.sleep(interval)
                bar.update(i)

        print(f"Среднее за {number_of_attempts} попыток(ки) успешных пингов = {numpy.mean(success) * 100 / package_count}%")
        logger.info(f"Среднее за {number_of_attempts} попыток(ки) успешных пингов = {numpy.mean(success) * 100 / package_count}%")
        logger.info(f"Скрипт завершен!")
    except Exception as Argument:
        logger.debug(Argument)


if __name__ == "__main__":
    main()