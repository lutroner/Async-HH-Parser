from pprint import pprint
import asyncio
import aiohttp
import time
from loguru import logger

HH_BASE_URL = 'https://api.hh.ru/vacancies'
PROGRAMMING_CATEGORY_ID = 96
SEARCH_PERIOD = 30
AREA_ID = 1
PROGRAMMING_LANGUAGES = ('Python', 'Java', 'Perl', 'JavaScript', 'C++', 'C#', 'Go', 'Ruby', 'Php', 'Rust')


def predict_rub_salary(vacancy) -> float or None:
    """Усредняем зарплаты в зависимости от того, указано ли "от" и/или "до\""""
    if vacancy['from'] and vacancy['to']:
        return (vacancy['from'] + vacancy['to']) / 2
    elif vacancy['from'] and vacancy['to'] is None:
        return vacancy['from'] * 1.2
    elif vacancy['from'] is None and vacancy['to']:
        return vacancy['to'] * 0.8
    else:
        return None


async def get_salary_by_language(language: str, session: aiohttp.ClientSession, page: int = 0) -> dict:
    vacancies = {}
    payload_page = {'professional_role': PROGRAMMING_CATEGORY_ID,
                    'period': SEARCH_PERIOD,
                    'area': AREA_ID,
                    'text': language,
                    'page': page
                    }
    async with session.get(HH_BASE_URL, data=payload_page) as response:
        response = await response.json()
        vacancies[language] = {'vacancies_found': response['found']}
        number_of_pages = response['pages']
        average_salary = 0
        vacancies_processed = 0
        for page in range(number_of_pages):
            payload_page['page'] = page
            async with session.get(HH_BASE_URL, data=payload_page) as resp:
                resp = await resp.json()
            for vacancy in resp['items']:
                try:
                    if predict_rub_salary(vacancy['salary']):
                        average_salary += int(predict_rub_salary(vacancy['salary']))
                        vacancies_processed += 1
                except TypeError:
                    logger.debug(f'Зарплата для вакансии "{vacancy["name"]}" не указана', )
        average_salary /= vacancies_processed
        vacancies[language].update({'vacancies_processed': vacancies_processed})
        vacancies[language].update({'average_salary': int(average_salary)})
        logger.info(f'Средняя ЗП по языку {language} равна: {int(average_salary)}')
    return vacancies


async def main() -> None:
    t_start = time.monotonic()
    async with aiohttp.ClientSession() as session:
        tasks = (get_salary_by_language(language, session) for language in PROGRAMMING_LANGUAGES)
        result = await asyncio.gather(*tasks)
        result = {i: item[i] for item in result for i in item}  # list of dict to dict of dicts
        pprint(result)
    print(f'Всего времени затрачено {time.monotonic() - t_start}')


if __name__ == '__main__':
    asyncio.run(main())
