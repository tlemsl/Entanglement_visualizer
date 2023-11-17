import pygame
import sys

class Circuit:
    class Gate:
        def __init__(self, blank):
            self.is_empty = True
            self.gate_type = None
            self.gate_obj = None
            self.blank_obj = blank

    def __init__(self, max_circuit_length):
        self.blank_list = []

        self.max_circuit_length = max_circuit_length
        self.add_qubit()

    def add_qubit(self):
        tmp_list = []
        for i in range(self.max_circuit_length):
            tmp_list.append(self.Gate(pygame.Rect(150+i*200,100+100*(1+len(self.blank_list)),100,50)))
        self.blank_list.append(tmp_list)

    def del_qubit(self):
        if(len(self.blank_list)==0):
            return None
        del self.blank_list[-1]
        for i in self.blank_list:
            for j in i:
                j.is_empty = True
                j.gate_type = None
                j.gate_obj = None

    def get_result(self):
        # get result of quntum circuit
        return None

    def get_entanglement(self):
        # get entanglement state of quntum circuit
        return None


# 초기화
pygame.init()

#회로 클래스 생성
circuit = Circuit(9)

# 화면 설정
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("qubit simulator")

# 색상 정의)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0 ,0 ,255)
GREEN = (0,255,0)

# 버튼 정의
button_rect_x = pygame.Rect(50, 50, 100, 50)
button_rect_y = pygame.Rect(200, 50, 100, 50)
button_rect_z = pygame.Rect(350, 50, 100, 50)

button_add_qubit = pygame.Rect(1200,20,200,50)
button_red_qubit = pygame.Rect(1200,90,200,50)
button_del_qubit = pygame.Rect(1500,25,400,100)



# 드래그 중인지 여부
dragging = False

# 물체가 빈칸 안에 들어갔는지 여부
object_in_empty = False

# 오브젝트 리스트
objects = []

# 폰트 초기화
font = pygame.font.Font(None, 36)

# 버튼 텍스트 생성
button_text_x = font.render("X-gate", True, WHITE)
button_text_rect_x = button_text_x.get_rect(center=button_rect_x.center)
button_text_y = font.render("Y-gate", True, WHITE)
button_text_rect_y = button_text_y.get_rect(center=button_rect_y.center)
button_text_z = font.render("Z-gate", True, WHITE)
button_text_rect_z = button_text_z.get_rect(center=button_rect_z.center)

button_add_qubit_text = font.render("Add qubit", True , WHITE)
button_add_qubit_text_rect = button_add_qubit_text.get_rect(center=button_add_qubit.center)

button_red_qubit_text = font.render("Del qubit", True , WHITE)
button_red_qubit_text_rect = button_red_qubit_text.get_rect(center=button_red_qubit.center)

button_del_qubit_text = font.render("Place gate here to delete", True , WHITE)
button_del_qubit_text_rect = button_del_qubit_text.get_rect(center=button_del_qubit.center)

#Gate 텍스트
gate_x_text = font.render("X", True, WHITE)
gate_y_text = font.render("Y", True, WHITE)
gate_z_text = font.render("Z", True, WHITE)


selected_obj = None

# 메인 루프
while True:
    screen.fill(WHITE)


    # 버튼 그리기
    pygame.draw.rect(screen, RED, button_rect_x)
    screen.blit(button_text_x, button_text_rect_x)

    pygame.draw.rect(screen, RED, button_rect_y)
    screen.blit(button_text_y, button_text_rect_y)

    pygame.draw.rect(screen, RED, button_rect_z)
    screen.blit(button_text_z, button_text_rect_z)

    pygame.draw.rect(screen, RED, button_add_qubit)
    screen.blit(button_add_qubit_text,button_add_qubit_text_rect)

    pygame.draw.rect(screen, RED, button_red_qubit)
    screen.blit(button_red_qubit_text,button_red_qubit_text_rect)

    pygame.draw.rect(screen, RED, button_del_qubit)
    screen.blit(button_del_qubit_text,button_del_qubit_text_rect)



    #빈칸 그리기
    for qubit in circuit.blank_list:
        for blank in qubit:
            pygame.draw.rect(screen,BLACK,blank.blank_obj)


    for obj,g_type, is_set in objects:
        if(not is_set):
            pygame.draw.rect(screen, BLUE, obj)
        else:
            pygame.draw.rect(screen, GREEN, obj)
        gate_type_rect = None
        if g_type =="X":
            gate_text_rect = gate_x_text.get_rect(center=obj.center)
            screen.blit(gate_x_text,gate_text_rect)
        elif g_type == "Y":
            gate_text_rect = gate_y_text.get_rect(center=obj.center)
            screen.blit(gate_y_text,gate_text_rect)
        elif g_type == "Z":
            gate_text_rect = gate_z_text.get_rect(center=obj.center)
            screen.blit(gate_z_text,gate_text_rect)







    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if gate is dragged
            for obj,g_type ,is_set in objects:
                if obj.collidepoint(event.pos):
                    dragging =True
                    selected_obj = obj
                    break

            # check gate generation button is pushed
            if button_rect_x.collidepoint(event.pos):
                new_object = pygame.Rect(50, 120, 100, 50)
                objects.append([new_object,"X", False])

            elif button_rect_y.collidepoint(event.pos):
                new_object = pygame.Rect(200, 120, 100, 50)
                objects.append([new_object,"Y", False])

            elif button_rect_z.collidepoint(event.pos):
                new_object = pygame.Rect(350, 120, 100, 50)
                objects.append([new_object,"Z", False])

            # add new qubit action
            elif button_add_qubit.collidepoint(event.pos):
                circuit.add_qubit()

            # del qubit action
            elif button_red_qubit.collidepoint(event.pos):
                circuit.del_qubit()
                objects=[]


        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False



            for qubit in circuit.blank_list:
                for blank in qubit:
                    if blank.is_empty:
                        for i in range(len(objects)):
                            if objects[i][0].colliderect(blank.blank_obj):
                                objects[i][0].topleft = blank.blank_obj.topleft
                                blank.gate_type = objects[i][1]
                                blank.gate_obj = objects[i][0]
                                blank.is_empty = False
                                objects[i][2] = True
                                break


                    else:
                        change_flag = True
                        change_idx = None
                        for i in range(len(objects)):
                            if objects[i][0] == blank.gate_obj:
                                change_idx = i
                                if objects[i][0].colliderect(blank.blank_obj):
                                    change_flag = False
                                break
                        if change_flag:
                            blank.is_empty = True
                            blank.gate_type = None
                            blank.gate_obj = None
                            if objects[change_idx][0].colliderect(button_del_qubit):
                                del objects[change_idx]
                            else:
                                objects[change_idx][2] = False





        elif event.type == pygame.MOUSEMOTION and dragging:
            selected_obj.move_ip(event.rel)




    pygame.display.flip()
