import pygame as pg
import sys
from .map import Map
from utils.settings import *
from utils.util_functions import draw_text,spawn_enemy_unit,spawn_ally_unit
from .camera import Camera
from .hud import Hud , Minimap
from .resource_manager import ResourceManager
from entities.units.worker import Herobrine
from .IA import *
from .py import handle_send
from vrai_reseau2.variable import stri
from vrai_reseau2 import variable
from vrai_reseau2.entities.buildings import *
from entities.buildings.enemybarrack import EnemyBarrack
from entities.buildings.enemyarchery_range import EnemyArchery_range
from entities.buildings.enemystable import EnemyStable
from entities.buildings.enemyarmory import EnemyArmory
from entities.buildings.enemyfarm import EnemyFarm
from vrai_reseau2.entities.units.worker import *
from entities.units.swordman import Swordman
from entities.units.worker import Worker
from entities.units.enemyunit import EnemyUnit
from entities.units.enemyworker import EnemyWorker
from entities.units.enemyswordman import EnemySwordman
from entities.units.enemybowman import EnemyBowman
from entities.units.enemyhorseman import EnemyHorseman




class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.cheat = CHEAT
        self.mapsize = WORLD_SIZE
        self.prop = False
        self.player = Player
        #victoire/defaite
        self.victoire = 1
        self.defaite = 1

        # entities
        self.entities = []

        # camera
        self.camera = Camera(self.width, self.height)
        self.camera.scroll.x = -int(31.6*WORLD_SIZE - 600)
        self.camera.scroll.y = WORLD_SIZE

    def initiate_resource_manager(self, start_resources_player, start_resources_AI):
        # resource manager
        # print("In initiate_resource_manager() :\n")
        # print(start_resources_player)
        # print(start_resources_AI)
        self.resource_manager = ResourceManager(start_resources_player, start_resources_AI)
        
    def initiate_hud(self):
        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height)

    def initiate_map(self):
        # Map
        self.map = Map(
            self.screen, self.resource_manager, self.entities, self.hud,
            self.mapsize, self.width, self.height, self.camera,self.player
        )
        self.minimap = Minimap(self.map, self.width,self.height,self.mapsize)
    
    #def initiate_IA(self):
        #self.IA = IA_class(self.map, self.resource_manager)



    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(100)
            if self.events():
                self.playing=False
                return True
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F11:  # condition de victoire
                    self.map.enemyTH.hp = 0




                if event.key == pg.K_F12: # condition de défaite
                    self.map.TH.hp = 0

                if event.key == pg.K_ESCAPE:
                    return True
                if self.cheat:
                    if event.key == pg.K_F1:
                        self.map.workers.append(Herobrine(self.map.map[self.map.ally_TH_x+1][self.map.ally_TH_y+1], self.map, self.map.resource_manager))
                        self.map.map[self.map.ally_TH_x+1][self.map.ally_TH_y+1]["troop"] = True

                    if event.key == pg.K_F2:
                        print("testsmiluation", self.map.map[2][15]["prop"])
                        #print("voici la valeur que j'ai recu",variable.stri)
                        #for n in self.resource_manager.resources:
                            #self.resource_manager.resources[n] +=10000


                    if event.key == pg.K_F3:
                        for n in self.resource_manager.resources:
                            if self.resource_manager.resources[n] + 10000 >= 0:
                                self.resource_manager.resources[n] += 10000
                            else:
                                self.resource_manager.resources[n] = 0
                        #handle_send("test2")

                    if event.key == pg.K_F4:
                        for i in range(len(GAME_SPEED)):
                            if self.map.GAME_SPEED==GAME_SPEED[i]:
                                x=i
                        if x < len(GAME_SPEED)-1:
                            self.map.GAME_SPEED=GAME_SPEED[x+1]
                        else: self.map.GAME_SPEED=GAME_SPEED[0]

                    if event.key == pg.K_F5:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [1] * len(self.map.vision_matrix[x])

                    if event.key == pg.K_F6:
                        vision_range = range(len(self.map.vision_matrix))
                        for x in vision_range:
                            self.map.vision_matrix[x] = [0] * len(self.map.vision_matrix[x])
                        for x in range(len(self.map.buildings)):
                            for y in range(len(self.map.buildings)):
                                if self.map.buildings[x][y] is not None and self.map.buildings[x][y].team==1:
                                    self.map.update_vision_matrix((x,y),self.map.buildings[x][y].fieldofview)
            # if event.type == pg.MOUSEBUTTONDOWN:

    def update(self):
        #print("stri",variable.stri)
        usable_string = variable.transform_string(variable.stri)
        #print(self.entities)
        #print("strimodifié",usable_string)
        x = variable.transform_string2(variable.stri)
        # print("testultime",x)
        #print("XO", x[0])
        #print("testsmiluation", self.map.map[2][15]["prop"])

        if x[0] == "can_i" and self.map.map[x[1][0]][x[1][1]]["prop"] == False:
            print("On a recu la chaine: ", x[0])

            handle_send("True")
            print("On renvoi TRUE")
            variable.stri = "end"
            #print(variable.stri)

        if x[0] == "can_i" and self.map.map[x[1][0]][x[1][1]]["prop"] == True:  # SI TRUE CE JOUEUR est le proprietaire unique
            print(x[0])
            print("IMPOSSIBLE DE CEDER LA PROPRIETE")

            handle_send("False")
            print("RENVOI DE FALSE")
            variable.stri = "end"

        # if variable.stri == "True":
        # self.prop = True

        for a in self.entities:
            if isinstance(a,EnemyWorker):
                if("worker_deplacement" == usable_string[0]):
                    if(a.tile['grid'] == [usable_string[1][0],usable_string[1][1]]):
                        print("FINALLDC")
                        a.go_close(self.map.map[usable_string[1][2]][usable_string[1][3]],[0])
                        #a.go_close(self.map.map[2][15],[0])
                        variable.stri = "end"
                        variable.to_mine = usable_string[1]
                        print("test1",variable.to_mine)

                """if ("minage," == variable.stri):
                    print("test2", variable.to_mine)
                    if (a.tile['grid'] == [variable.to_mine[0], variable.to_mine[1]]):
                        print(usable_string)
                        a.mine(self.map.map[variable.to_mine[2]][variable.to_mine[3]])
                        variable.stri = "end"""
                if("minage"==usable_string[0]):
                    if (a.tile['grid'] == [usable_string[1][0], usable_string[1][1]]):
                        a.mine(self.map.map[usable_string[1][2]][usable_string[1][3]])
                        variable.stri = "end"

                    print('we entetered attack')
                    print("depart de l'attak",[usable_string[1][0], usable_string[1][1]])
                    print("case a attaqué",[usable_string[1][2], usable_string[1][3]])
                    if(a.tile['grid'] == [usable_string[1][0], usable_string[1][1]]):
                        for b in self.entities:
                            print(b)

                            if isinstance(b,Worker):
                                print("est ce que b est un worker")
                                if b.tile['grid'] == [usable_string[1][2], usable_string[1][3]]:
                                    print("tu va attaquer j'espere la ")
                                    b.attack(a)
                                    print("tu attaque pas enculer ?")

                if ("die" == usable_string[0]):
                    if(a.tile['grid'] == [usable_string[1][0], usable_string[1][1]]):
                        a.die()













        self.camera.update()
        for e in self.entities:
            e.update()
            self.hud.end_V(self.screen)
        self.hud.update()
        self.map.update(self.camera)
        #print("voici la valeur que j'ai recu",variable.stri)
        if variable.text=="can_i" :
            print(variable.stri)
            handle_send("True")
            variable.stri = "end"
        """if variable.a ==1:
            ent = Stable((7,7), self.map.resource_manager, self.map, self.map.hud)
            self.map.place_building(ent, (7,7))
            variable.a==0"""


        if usable_string[0]== "Barrack" :
            print('entity identified')
            ent = EnemyBarrack(usable_string[1], self.map.resource_manager, self.map)
            self.map.place_building(ent, usable_string[1])
            variable.stri = "end"
            #variable.str_test = ''

        if usable_string[0] == "Armory" :
            print('entity identified')
            ent = EnemyArmory(usable_string[1], self.map.resource_manager, self.map)
            self.map.place_building(ent, usable_string[1])
            variable.stri = "end"

        if usable_string[0]== "Archery range" :
            print('entity identified')
            ent = EnemyArchery_range(usable_string[1], self.resource_manager, self.map)
            self.map.place_building(ent, usable_string[1])
            variable.stri = "end"

        if usable_string[0]== "Stable" :
            print('entity identified')
            ent = EnemyStable(usable_string[1], self.map.resource_manager, self.map)
            self.map.place_building(ent, usable_string[1])
            variable.stri = "end"
        if usable_string[0] == "worker":
            print("TESTULTIMATE")
            ent = EnemyWorker(self.map.map[usable_string[1][0]][usable_string[1][1]], self.map, self.resource_manager)
            # self.map.place_worker(ent)
            self.map.workers.append(ent)
            variable.stri = "end"
        if usable_string[0] == "horseman":
            ent = EnemyHorseman(self.map.map[usable_string[1][0]][usable_string[1][1]], self.map, self.resource_manager)
            self.map.place_worker(ent)
            variable.stri = "end"
        if usable_string[0] == "swordman" :
            ent = EnemySwordman(self.map.map[usable_string[1][0]][usable_string[1][1]], self.map, self.resource_manager)
            self.map.place_worker(ent)
            variable.stri = "end"
        if usable_string[0] == "bowman":
            ent = EnemyBowman(self.map.map[usable_string[1][0]][usable_string[1][1]], self.map, self.resource_manager)
            self.map.place_worker(ent)
            variable.stri = "end"




        #self.IA.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.map.draw(self.screen, self.camera)
        self.hud.draw(self.screen)
        self.minimap.update(self.screen)
        if self.map.enemyTH.hp <= 0 and self.victoire :  # condition de victoire
            #print("VICTORY")
            self.defaite = 0
            mouse_action = pg.mouse.get_pressed()
            self.map.GAME_SPEED = 1000000000000
            self.hud.end_V(self.screen)
            if mouse_action[0]:
                sys.exit()



        if self.map.TH.hp <= 0 and self.defaite :  # condition de défaite
            #print("DEFAITE")
            self.victoire = 0

            mouse_action = pg.mouse.get_pressed()
            self.map.GAME_SPEED = 1000000000000
            self.hud.end_D(self.screen)
            if mouse_action[0]:
                sys.exit()



        draw_text(
            self.screen,
            'fps={}'.format(round(self.clock.get_fps())),
            25,
            (255, 255, 255),
            (10, 1)
        )
        if self.cheat:
            draw_text(self.screen,"Cheats ON",25,(255, 255, 255),(75, 1))
            draw_text(self.screen,"F1 Herobrine | ",25,(255, 255, 255),(10, 20))
            draw_text(self.screen,"F2-F3 +-10k resources | ",25,(255, 255, 255),(130, 20))
            draw_text(self.screen,"F4 Game speed : " + GAME_SPEED_NAMES[self.map.GAME_SPEED] + " | ",25,(255, 255, 255),(320, 20))
            draw_text(self.screen,"F5 No fog | ",25,(255, 255, 255),(555, 20))
            draw_text(self.screen,"F6 Reset fog | ",25,(255, 255, 255),(645, 20))

        pg.display.flip()
