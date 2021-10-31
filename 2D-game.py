import arcade

#constents for window size, and name of game
screen_width = 1000
screen_height = 600
screen_title = "Cube Platformer"

#constents for sprites
charcter_scale = 1
tile_scale = .5
rupee_scale = .2

#const for movement
player_speed = 5

#const gravity
grav = 1
jump_speed = 20

class myGame(arcade.Window):
    
    def __init__(self):
        super().__init__(screen_width,screen_height,screen_title)

        self.scene = None

        self.player_sprite = None

        # physics engine
        self.physics_engine = None

        self.camera = None

        self.collect_coin_sound = arcade.load_sound("OOT_Get_Rupee.wav")
        self.jump_sound = arcade.load_sound("OOT_AdultLink_Jump1.wav")
        
        
        self.background = None
        # arcade.set_background_color(arcade.color.RED)

    
    def setup(self):

        self.scene = arcade.Scene()
        # setup for camera
        self.camera = arcade.Camera(self.width, self.height)

        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("walls", use_spatial_hash=True)

        self.background = arcade.load_texture("desert_back.png")

        image_source = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.player_sprite = arcade.Sprite(image_source, charcter_scale)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("player", self.player_sprite)


        # Makes ground for game
        for x in range(0,1250,64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", tile_scale)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

            coordinate_list = [[512,96], [256,96], [768,96]]
            for coordinate in coordinate_list:
                wall = arcade.Sprite (":resources:images/tiles/bridgeB.png", tile_scale)
                wall.position = coordinate
                self.scene.add_sprite("Walls", wall)

                for x in range(130,1250,256):
                    coin = arcade.Sprite("purple_rupee.png", rupee_scale)
                    coin.center_x = x
                    coin.center_y = 96
                    self.scene.add_sprite("Coins", coin)

            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.scene.get_sprite_list("Walls"), grav)
    def on_draw(self):

        arcade.start_render()

        self.camera.use()

        arcade.draw_lrwh_rectangle_textured(0, 65,screen_width, screen_height, self.background)

        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = jump_speed
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -player_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = player_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delt_time):

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Coins"))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        self.center_camera_to_player()


def main():
        window = myGame()
        window.setup()
        arcade.run()
if __name__ == "__main__":
    main()