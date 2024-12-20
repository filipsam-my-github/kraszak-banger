import sys

import pygame
import moderngl
from array import array

pygame.init()

screen = pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((800,600))

ctx = moderngl.create_context()

clock = pygame.time.Clock()


img = pygame.image.load(f"graphics/animations/kraszaks_heading_down/Kraszaks-Heading-Down-0.png")                
img = pygame.transform.scale(img, (img.get_width() * 10, img.get_height() * 10))

quad_buffer = ctx.buffer(data=array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
]))

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main(){
    vec2 circle_centre;
    circle_centre = vec2(0.5, 0.5);
    
    float red;
    float green;
    float blue;
    
    red = texture(tex, uvs).r;
    green = texture(tex, uvs).g;
    blue = texture(tex, uvs).b;
    
    float disc = length(uvs - circle_centre);
    
    disc = 5*disc;
    
    if (disc > 1){
        disc = 1;
    }
    
    disc = abs(disc - 1.0);
    
    
    
    
    
    f_color = vec4(red*disc, green*disc, blue*disc, 1.0);
}
'''

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, '2f 2f', 'vert', 'texcoord')])

def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = 'BGRA'
    tex.write(surf.get_view('1'))
    
    return tex
    
    

while True:
    display.fill((0,255,0))
    display.blit(img, pygame.mouse.get_pos())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program['tex'] = 0
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    
    pygame.display.flip()
    
    frame_tex.release()
    
    clock.tick(60)