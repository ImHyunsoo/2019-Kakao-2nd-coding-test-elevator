import lib

def p0_simulator():
    user = 'tester'
    problem = 0
    count = 4

    ret = lib.start(user, problem, count)
    token = ret['token']
    print('Token for %s is %s' % (user, token))

    tmp_elevator = ['STOPPED'] * count

    while True:
        oncall_data = lib.oncalls(token)

        if oncall_data['is_end']:
            break

        command_list = []
        for elevator in oncall_data['elevators']:
            tmp_command = {}
            tmp_command['elevator_id'] = elevator['id']


            if elevator.get('status') == 'STOPPED':
                # 현재층에 콜이 있으면 OPEN 명령 내림
                if lib.b_exit_call(elevator) or lib.b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'OPEN'

                # 현재, 위, 아래층에 태울 콜이 없다면, STOP
                elif not lib.b_upstairs_call(oncall_data, elevator) and not lib.b_downstairs_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'
                    tmp_elevator[elevator['id']] = 'STOPPED'

                # 멈추기 전에 올라가고 있는 상태였을 때, 위층에 콜이 있다면 UP, 아래층에 콜 있다면 DOWN, 위아래 둘 다 콜이 없다면 STOP
                elif tmp_elevator[elevator['id']] == 'UPWARD':
                    if lib.b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    elif lib.b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'
                    else: tmp_command['command'] = 'STOP'

                # 멈추기 전에 내려가고 있는 상태였을 때, 아래층에 콜이 있다면 DOWN, 위층에 콜이 있다면 UP, 위아래 둘다 콜이 없다면 STOP
                elif tmp_elevator[elevator['id']] == 'DOWNWARD':
                    if lib.b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'
                    elif lib.b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    else: tmp_command['command'] = 'STOP'

                # 콜이 없어서 전에도 멈춘 상태였었고, 위, 아래 층에 동시 콜이 생기면 더 가까운 쪽으로 UP or DOWN, 위층에만 콜이 생기면 UP, 아래층에만 콜이 생기면 DOWN
                elif tmp_elevator[elevator['id']] == 'STOPPED':
                    if lib.b_upstairs_call(oncall_data, elevator) and lib.b_downstairs_call(oncall_data, elevator):
                        tmp_command['command'] = lib.closer_call_move(oncall_data, elevator)
                    if lib.b_upstairs_call(oncall_data, elevator): tmp_command['command'] = 'UP'
                    if lib.b_downstairs_call(oncall_data, elevator): tmp_command['command'] = 'DOWN'


            elif elevator.get('status') == 'UPWARD':
                # 현재 층에 콜이 있다면, STOP
                if lib.b_exit_call(elevator) or lib.b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'

                # 현재 층에 콜이 없다면, UP
                else: tmp_command['command'] = 'UP'

                # 올라가고 있는 엘베 상태 저장
                tmp_elevator[elevator['id']] = 'UPWARD'


            elif elevator.get('status') == "DOWNWARD":
                # 현재 층에 콜이 있다면, STOP
                if lib.b_exit_call(elevator) or lib.b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'STOP'

                # 현재 층에 콜이 없다면, DOWN
                else: tmp_command['command'] = 'DOWN'

                # 내려가고 있는 엘베 상태 저장
                tmp_elevator[elevator['id']] = 'DOWNWARD'


            elif elevator.get('status') == 'OPENED':
                # 내려줄 콜 있으면 EXIT
                if lib.b_exit_call(elevator):
                    tmp_command['command'] = 'EXIT'
                    exit_list = lib.exit_call(elevator)
                    tmp_command['call_ids'] = exit_list

                # 태울 콜 있으면 ENTER
                elif lib.b_enter_call(oncall_data, elevator):
                    tmp_command['command'] = 'ENTER'
                    enter_list = lib.enter_call(oncall_data, elevator)
                    tmp_command['call_ids'] = enter_list

                # 내려주거나 태울 콜 없으면 CLOSE
                else: tmp_command['command'] = 'CLOSE'

            command_list.append(tmp_command)

        cmds = {}
        cmds['commands'] = command_list
        print(lib.action(token, cmds['commands']))


if __name__ == '__main__':
    p0_simulator()
