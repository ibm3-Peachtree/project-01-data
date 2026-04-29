# project-01-data

## session_summary.json
### key 정보
- title : 세션 제목
- date : 세션 날짜
- speakers : 강연자들 
  - 'img' : 강연자 사진
  - 'introduction' : 강연자 정보
  - 'name' : 이름
  - 'position' : 직책
  - 'organization' : 소속
- video_url : 비디오 링크
- description : 세션 설명
- summary : 요약
- kor_description : 세션 설명 한국어 번역

### 데이터 예시
```json
{
    "title": "Red Teaming AI Systems", 
    "date": "2024-03-08 00:00:00", 
    "category": ["Expert AI Training", "AI Literacy", "AI Research"], 
    "speakers": [
        {
            "img": "https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/openai/lama-69540054-6181-44bd-b853-3c9cc594a5ca-1687544964148.png?fit=scale-down&width=320", 
            "introduction": "Lama Ahmad is on the Policy Research team at OpenAI, where she leads efforts on external assessments of the impacts of AI systems on society. Her work includes leading the Researcher Access Program, OpenAI's red teaming efforts, third party assessment and auditing, as well as public input projects.", 
            "name": "Lama Ahmad", 
            "position": "Policy Researcher", 
            "organization": "OpenAI"
        }
    ], 
    "video_url": "https://vimeo.com/920666106", 
    "description": "In a recent talk at OpenAI, Lama Ahmad shared insights into OpenAI’s Red Teaming efforts, which play a critical role in ensuring the safety and reliability of AI systems. Hosted by Natalie Cone, OpenAI Forum’s Community Manager, the session opened with an opportunity for audience members to participate in cybersecurity initiatives at OpenAI...", 
    "summary": "OpenAI의 Lama Ahmad는 AI 시스템의 안전과 신뢰성 확보를 위한 '레드 티밍'의 중요성을 강조했습니다. 이는 취약점, 유해 출력 등 위험을 식별하는 구조화된 과정으로, 인간 전문가와 자동화 시스템을 결합하여 개발 생애 주기 전 반에 걸쳐 지속적인 위험 평가가 이루어져야 함을 역설했습니다.", 
    "kor_description": "AI Forum 한국인 참가자 여러분께,\n\n 아래는 OpenAI에서 진행된 세션 강의 내용의 핵심 번역입니다.\n\n---\n\n### **OpenAI의 AI 시스템 안전 및 신뢰성 확보 노력: \'레드 팀(Red Teaming)\' 활동에 대한 통찰**\n\n최근 OpenAI에서 열린 강연에서 **라마 아흐마드(Lama Ahmad)**는 AI 시스템의 안전성과 신뢰성을 보장하는 데 핵심적인 역할을 하는 OpenAI의 \'레드 팀(Red Teaming)\' 활동에 대한 통찰력을 공유했습니다. ..."
}
```

## speakers.json
### key 정보
- 처음 json key들 : 사람들 이름
```python
dict_keys(['Lama Ahmad', 'Hunter Lightman', 'Terence Tao', 'Ilya Sutskever', 'Daniel Selsam', 'Jakub Pachocki', 'Nathan Chappell', 'Dupé Ajayi', 'Jody Britten', 'Allison Fine', 'Anne Murphy', 'Gayle Roberts', 'Scott Rosenkrans', 'Woodrow Rosenbaum', 'Greg Niemeyer', 'Natalie Cone', 'Anton Maximov PhD', 'Lois Newman', 'Joshua Achiam', 'Chris Nicholson', 'Jason Kwon', 'Claudia von Vacano', 'Gašper  Beguš', 'Kevin Weil', 'Ronnie Chatterji', 'Siya Raj Purohit', 'Jake Cook', 'Teddy Lee', 'Kevin Feng', 'Andrew Konya', 'Sam Altman', 'David Kirtley', 'Jason Horne', 'Jaci Jenkins Lindburg', 'Axel Persaud', 'David Brubaker', 'Leah Belsky', "Ann O'Leary", 'Conor Grennan', 'Matt Lewis', 'Aaron Wilkowitz', 'Dr. Ahmed Elgammal', 'Erik Brynjolfsson', 'Joaquin  Quiñonero Candela', 'Chi-kwan (CK) Chan', 'David Deming', 'Mark Murray', 'Daniel Miessler', 'Joel Parish', 'Saffron Huang', 'Divya Siddarth', 'Mark Chen', 'James  Donovan', 'Shafi Goldwasser', 'Roderick Purwana', 'Miles Brundage', 'Andrew Mayne', 'Kevin Alwell', 'James Hills', 'David Autor', 'Tyna Eloundou', 'Joseph Fuller', 'Nate  Gross', 'James  Hairston', 'Kate Rouch', 'Casey Cuny', 'Red Avila', 'Sarah Warkov', 'Dr. Karin Kimbrough', 'Shibani Santurkar', 'Alex Martin Richmond', 'Daniel Rock', 'Gregor Schubert', 'Collin Burns', 'Pavel Izmailov', 'Brian Spears', 'Jacqueline Hehir'])
```
- `사람 이름` 으로 접근하면 정보들 접근 가능
```python
with open ('./speakers.json', 'r', encoding='utf-8') as rj :
    speakers = json.load(rj)

speakers['Lama Ahmad']
```
- name : 이름
- img : 강연자 이미지
- introduction : 강연자 소개(영어)
- position : 직책
- organization : 소속
- history : 강연자 연혁(Introduction으로 AI 생성)
  - year : 연도 (임의 생성)
  - content : 내용 (임의로 나눔)

### 데이터 예시
```json
"Lama Ahmad" : {
    "name": "Lama Ahmad", 
    "img": "https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/openai/lama-69540054-6181-44bd-b853-3c9cc594a5ca-1687544964148.png?fit=scale-down&width=320", 
    "introduction": "Lama Ahmad is on the Policy Research team at OpenAI, where she leads efforts on external assessments of the impacts of AI systems on society. Her work includes leading the Researcher Access Program, OpenAI's red teaming efforts, third party assessment and auditing, as well as public input projects.",
    "position": "Policy Researcher", 
    "organization": "OpenAI", 
    "history": 
        {
            "year": [2022, 2023, 2024, 2024], 
            "content": [
                "OpenAI 정책 연구팀 정책 연구원", 
                "AI 시스템의 사회적 영향에 대한 외부 평가 노력 주도", 
                "연구자 접근 프로그램 리더", 
                "OpenAI의 레드팀 노력 및 타사 평가/감사 주도"
            ]
        }
}
```