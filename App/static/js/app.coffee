window.requestAnimFrame = ((callback) ->
    return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    (callback) ->
        window.setTimeout(callback, 1000 / 60);
)()

canvas = document.getElementById('header_canvas')
context = canvas.getContext('2d')

header = document.getElementById('header')
canvas.height = header.clientHeight
canvas.width = header.clientWidth
pulser = 0

style_type = Math.random()

update = () ->
    context.clearRect(0, 0, canvas.width, canvas.height)

    for i in [0...500] by 4
        context.beginPath()
        context.moveTo((0.5*i)+Math.abs(i*Math.sin(pulser)), 0)
        context.lineTo((0.5*i)+Math.abs(i*Math.sin(pulser)), canvas.width)
        context.strokeStyle = "#000"
        if style_type < 0.5
            context.rotate(1)
        context.stroke()

    pulser+=0.005;

    requestAnimFrame(() -> 
        update()
    )

requestAnimFrame(() -> 
    update()
)
