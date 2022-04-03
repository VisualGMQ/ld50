import framework
import welcome_scene
import game_scene


if __name__ == '__main__':
    theFramework = framework.Framework()

    theFramework.Init(welcome_scene.WelcomeScene())
    # theFramework.Init(game_scene.GameScene())
    theFramework.Run()
    theFramework.Shutdown()
