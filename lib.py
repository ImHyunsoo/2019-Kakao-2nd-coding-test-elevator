import requests

INF = 1e+9
url = 'http://localhost:8000'


def start(user, problem, count):
    uri = url + '/start' + '/' + user + '/' + str(problem) + '/' + str(count)
    return requests.post(uri).json()


def oncalls(token):
    uri = url + '/oncalls'
    return requests.get(uri, headers={'X-Auth-Token': token}).json()


def action(token, cmds):
    uri = url + '/action'
    return requests.post(uri, headers={'X-Auth-Token': token}, json={'commands': cmds}).json()


# 엘베 최대 수용 8명이 다 찼는지 여부
def b_elev_full(elevator):
    if len(elevator['passengers']) == 8:
        return True
    return False

# 현재 층에서 더 가까이 있는 콜쪽으로 진행방향 설정
def closer_call_move(oncall_data, elevator):
    # 가장 가까운 위층과의 거리
    up_min_dist = INF
    for call in elevator["passengers"]:
        if call['end'] > elevator['floor']:
            dist = call['end'] - elevator['floor']
            if up_min_dist > dist:
                up_min_dist = dist
    if not b_elev_full(elevator):  # 엘베 정원이 다 차지 않은 경우, 태우는 콜과의 최단 거리 계산함
        for call in oncall_data['calls']:
            if call['start'] > elevator['floor']:
                dist = call['start'] - elevator['floor']
                if up_min_dist > dist:
                    up_min_dist = dist

    # 가장 가까운 아래층과의 거리
    down_min_dist = INF
    for call in elevator["passengers"]:
        if call['end'] < elevator['floor']:
            dist = elevator['floor'] - call['end']
            if down_min_dist > dist:
                down_min_dist = dist
    if not b_elev_full(elevator):  # 엘베 정원이 다 차지 않은 경우, 태우는 콜과의 최단 거리 계산함
        for call in oncall_data['calls']:
            if call['start'] < elevator['floor']:
                dist = elevator['floor'] - call['start']
                if down_min_dist > dist:
                    down_min_dist = dist

    if up_min_dist < down_min_dist:
        return 'UP'
    else:
        return 'DOWN'

# 위층에 내려주거나 태울 콜이 있는지 여부
def b_upstairs_call(oncall_data, elevator):
    for call in elevator["passengers"]:
        if call['end'] > elevator['floor']:
            return True
    for call in oncall_data['calls']:
        if call['start'] > elevator['floor']:
            if b_elev_full(elevator): # 엘베 정원이 다 찼으면 태우는 콜은 무시할 수 있도록 False 반환
                return False
            return True
    return False

# 아래층에 내려주거나 태울 콜이 있는지 여부
def b_downstairs_call(oncall_data, elevator):
    for call in elevator["passengers"]:
        if call['end'] < elevator['floor']:
            return True
    for call in oncall_data['calls']:
        if call['start'] < elevator['floor']:
            if b_elev_full(elevator): # 엘베 정원이 다 찼으면 태우는 콜은 무시할 수 있도록 False 반환
                return False
            return True
    return False

# 현재 층에 내려줄 콜이 있는지 여부
def b_exit_call(elevator):
    for call in elevator['passengers']:
        if call['end'] == elevator['floor']:
            return True
    return False

# 현재 층에 태워줄 콜이 있는지 여부
def b_enter_call(oncall_data, elevator):
    for call in oncall_data['calls']:
        if call['start'] == elevator['floor']:
            if b_elev_full(elevator): # 엘베 정원이 다 찼으면 태우는 콜은 무시할 수 있도록 False 반환
                return False
            return True
    return False

# 내려줄 콜 리스트 반환
def exit_call(elevator):
    exit_call_list = []
    for call in elevator['passengers']:
        if call['end'] == elevator['floor']:
            exit_call_list.append(call['id'])
    return exit_call_list

# 태워줄 콜 리스트 반환
def enter_call(oncall_data, elevator):
    enter_call_list = []
    for call in oncall_data['calls']:
        if call['start'] == elevator['floor']:
            if len(elevator['passengers']) + len(enter_call_list) < 8: # 엘베 정원을 초과하지 않도록 태울 승객 리스트를 추가
                enter_call_list.append(call['id'])
            else: return enter_call_list
    return enter_call_list

