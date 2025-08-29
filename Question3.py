import turtle

def koch_curve(t, length, depth, inward=True):
    if depth == 0:
        t.forward(length)
    else:
        length /= 3
        if inward:
            koch_curve(t, length, depth-1, inward)
            t.left(60)
            koch_curve(t, length, depth-1, inward)
            t.right(120)
            koch_curve(t, length, depth-1, inward)
            t.left(60)
            koch_curve(t, length, depth-1, inward)

def fractal_polygon(sides, length, depth, inward=True):
    window = turtle.Screen()
    window.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)

    angle = 360 / sides

    for _ in range(sides):
        koch_curve(t, length, depth, inward)
        t.left(angle)

    window.mainloop()

sides = int(input("Enter the number of sides: "))
length = int(input("Enter the side length: "))
depth = int(input("Enter the recursion depth: "))
fractal_polygon(sides, length, depth,)
