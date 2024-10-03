import requests
import argparse


class CVESearcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def search_by_keyword(self, keyword, show_details=False):
        url = f"{self.base_url}?keywordSearch={keyword}"
        headers = {
            'apiKey': self.api_key
        }

        # API 요청 보내기
        response = requests.get(url, headers=headers)

        # 응답 처리
        if response.status_code == 200:
            data = response.json()
            total_results = data.get('totalResults', 0)
            if total_results > 0:
                print(f"{keyword} 라이브러리는 NVD에서 {total_results}개의 취약점이 검출되었습니다.")

                # 옵션에 따라 세부 정보 출력
                if show_details:
                    vulnerabilities = data.get('vulnerabilities', [])
                    for vulnerability in vulnerabilities:
                        cve = vulnerability.get('cve', {})
                        cve_id = cve.get('id', 'N/A')
                        descriptions = cve.get('descriptions', [])
                        description_text = next(
                            (d['value'] for d in descriptions if d['lang'] == 'en'),
                            '설명이 제공되지 않았습니다.'
                        )
                        print(f"\nCVE ID: {cve_id}")
                        print(f"설명: {description_text}")
            else:
                print(f"{keyword} 라이브러리는 NVD에서 취약점이 검출되지 않았습니다")
        else:
            print(f"NVD에서 정보를 가져오지 못했습니다. API 요청 실패: {response.status_code}")


# main 함수로 CLI에서 실행 가능하도록 설정
def main():
    parser = argparse.ArgumentParser(description='CVE 검색 라이브러리')
    parser.add_argument('--api_key', required=True, help='NVD API Key ex) --api_key apikey')
    parser.add_argument('--keyword', required=True, help='검색할 키워드 ex) --keyword urllib3')
    parser.add_argument('--details', action='store_true', help='세부 취약점 정보를 출력할지 여부')

    args = parser.parse_args()

    searcher = CVESearcher(args.api_key)
    searcher.search_by_keyword(args.keyword, show_details=args.details)


if __name__ == "__main__":
    main()
