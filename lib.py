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

# 현재 층에서 더 가까이 있는 콜로 이동
def closer_call_move(oncall_data, elevator):
    # 가장 가까운 위층과의 거리
    up_min_dist = INF
    for call in elevator["passengers"]:
        if call['end'] > elevator['floor']:
            dist = call['end'] - elevator['floor']
            if up_min_dist > dist:
                up_min_dist = dist
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
            return True
    return False

# 아래층에 내려주거나 태울 콜이 있는지 여부
def b_downstairs_call(oncall_data, elevator):
    for call in elevator["passengers"]:
        if call['end'] < elevator['floor']:
            return True
    for call in oncall_data['calls']:
        if call['start'] < elevator['floor']:
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
            enter_call_list.append(call['id'])
    return enter_call_list


def p0_simulator():
    user = 'tester'
    problem = 0
    count = 1

    ret = start(user, problem, count)
    token = ret['token']
    print('Token for %s is %s' % (user, token))

    tmp_elevator = ['STOPPED'] * count

    while True:
        oncall_data = oncalls(token)

        if oncall_data['is_end']:
            break

        command_list = []
        for elevator in oncall_data['elevators']:
            tmp_command = {}
            tmp_command['elevator_id'] = elevator['id']


            if elevator.get('status') == 'STOPPED':
                # 현재층에 콜이 있으면 OPEN 명령 내림
                if b_exit_call(elevator) or b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'OPEN'

                # 현재, 위, 아래층에 태울 콜이 없다면, STOP
                elif not b_upstairs_call(oncall_data, elevator) and not b_downstairs_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'
                    tmp_elevator[elevator['id']] = 'STOPPED'

                # 멈추기 전에 올라가고 있는 상태였을 때, 위층에 콜이 있다면 UP, 아래층에 콜 있다면 DOWN, 위아래 둘 다 콜이 없다면 STOP
                elif tmp_elevator[elevator['id']] == 'UPWARD':
                    if b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    elif b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'
                    else: tmp_command['command'] = 'STOP'

                # 멈추기 전에 내려가고 있는 상태였을 때, 아래층에 콜이 있다면 DOWN, 위층에 콜이 있다면 UP, 위아래 둘다 콜이 없다면 STOP
                elif tmp_elevator[elevator['id']] == 'DOWNWARD':
                    if b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'
                    elif b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    else: tmp_command['command'] = 'STOP'

                # 콜이 없어서 전에도 멈춘 상태였었고, 위, 아래 층에 동시 콜이 생기면 더 가까운 쪽으로 UP or DOWN, 위층에만 콜이 생기면 UP, 아래층에만 콜이 생기면 DOWN
                elif tmp_elevator[elevator['id']] == 'STOPPED':
                    if b_upstairs_call(oncall_data, elevator) and b_downstairs_call(oncall_data, elevator):
                        tmp_command['command'] = closer_call_move(oncall_data, elevator)
                    if b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    if b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'


            elif elevator.get('status') == 'UPWARD':
                # 현재 층에 콜이 있다면, STOP
                if b_exit_call(elevator) or b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'

                # 현재 층에 콜이 없다면, UP
                else: tmp_command['command'] = 'UP'

                # 올라가고 있는 엘베 상태 저장
                tmp_elevator[elevator['id']] = 'UPWARD'


            elif elevator.get('status') == "DOWNWARD":
                # 현재 층에 콜이 있다면, STOP
                if b_exit_call(elevator) or b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'

                # 현재 층에 콜이 없다면, DOWN
                else: tmp_command['command'] = 'DOWN'

                # 내려가고 있는 엘베 상태 저장
                tmp_elevator[elevator['id']] = 'DOWNWARD'


            elif elevator.get('status') == 'OPENED':
                # 내려줄 콜 있으면 EXIT
                if b_exit_call(elevator):
                    tmp_command['command'] = 'EXIT'
                    exit_list = exit_call(elevator)
                    tmp_command['call_ids'] = exit_list

                # 태울 콜 있으면 ENTER
                elif b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'ENTER'
                    enter_list = enter_call(oncall_data, elevator)
                    tmp_command['call_ids'] = enter_list

                # 내려주거나 태울 콜 없으면 CLOSE
                else: tmp_command['command'] = 'CLOSE'

            command_list.append(tmp_command)

        cmds = {}
        cmds['commands'] = command_list
        print(action(token, cmds['commands']))