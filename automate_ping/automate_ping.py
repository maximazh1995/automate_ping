from pythonping import ping
import time
import numpy
import click


def ping_server(target_ip, package_size, package_count):
    count_of_success_packages = 0
    response_list = ping(target_ip, size=package_size, count=package_count, verbose = True)
    for response in response_list:
        if response.success:
            count_of_success_packages += 1
    return count_of_success_packages


@click.command()
@click.argument('target_ip')
@click.argument('package_size')
def main(target_ip, package_size):
    # target_ip = '8.8.8.8'  # целевой адрес
    # package_size = 60  # размер пакета (без учета заголовка ICMP - 8 байт)
    package_count = 20  # количество icmp пакетов в одну попытку
    number_of_attempts = 3  # количество попыток
    success = [0] * number_of_attempts  # массив для хранения количества успешных попыток
    interval = 5  # интервал между попытками в секундах

    for i in range(0, number_of_attempts):
        success[i] = ping_server(target_ip, int(package_size), package_count)
        time.sleep(interval)

    print(f"Среднее за {number_of_attempts} попыток(ки) успешных пингов = {numpy.mean(success) * 100 / package_count}%")


if __name__ == "__main__":
    main()