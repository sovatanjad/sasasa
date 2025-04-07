from random import randint
import  pygame

from GameObject import GameObject

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

class GameObject:
    '''Базовый класс для игровых объектов.'''

    def __init__(self):
        self.position = None
        self.body_color = None

    def draw(self):
        '''Метод для отображения объекта.'''
        raise NotImplementedError('Метод draw должен быть переопределен.')

class Apple(GameObject):
    '''Класс описывающий яблоко которое сьедается змеей'''
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        '''Рандомно задает позицию яблока на игровом поле'''
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        '''Изображает яблочко на экране.'''
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class  Snake(GameObject):
    '''Класс змейки которая перемещается по игровому полю.'''

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        '''Обнавляет новое направление движение змейки.'''
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        '''Двигает змейку в новом направлении.'''
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * GRID_SIZE)
        new_head_y = (head_y + self.direction[1] * GRID_SIZE)
        #Проверка на выход за границы.
        if new_head_x < 0 or new_head_x >= SCREEN_WIDTH or new_head_y < 0 or new_head_y >= SCREEN_HEIGHT:
            self.reset()
            return
        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        '''Изображает змейку на иг поле.'''
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        '''Возвращает новое положение головы змейки.'''
        return self.positions[0]

    def reset(self):
        '''Сброс состояния змейки к начальному.'''
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None

def handle_keys(snake):
    '''Обрабатывает клавиши и обновляет направление змеи.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

def main():
    '''Главная функция для запуска.'''
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        # Очистка экрана и отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()