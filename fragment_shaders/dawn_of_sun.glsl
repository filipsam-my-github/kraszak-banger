#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main(){
    vec2 circle_centre;
    circle_centre = vec2(0.5, 0.7);
    
    float red;
    float green;
    float blue;
    
    red = texture(tex, uvs).r;
    green = texture(tex, uvs).g;
    blue = texture(tex, uvs).b;
    
    float disc = length(uvs - circle_centre);
    
    disc = (disc / (0.25 + disc));
    
    if (disc > 1){
        disc = 1;
    }
    
    disc = abs(disc - 1.0);
    
    f_color = vec4(red*disc, green*disc, blue*disc, 1.0);
}