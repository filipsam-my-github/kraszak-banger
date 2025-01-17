#version 330 core

uniform sampler2D tex;
uniform float transposition_shader_multiplayer;

in vec2 uvs;
out vec4 f_color;

void main(){
    float adjusted_multiplayer = abs(transposition_shader_multiplayer);

    vec2 circle_centre;
    circle_centre = vec2(0.5, 0.7);
    
    float red;
    float green;
    float blue;
    
    red = texture(tex, uvs).r;
    green = texture(tex, uvs).g;
    blue = texture(tex, uvs).b;
    
    float disc = length(uvs - circle_centre);
    
    disc = 2*disc;
    
    if (disc > 1){
        disc = 1;
    }

    
    
    disc = abs(disc - 1.0)*adjusted_multiplayer;
    float old_disc = disc;


    disc = max(0.0,sqrt(pow(disc,5)));
    disc = min(disc,sqrt(pow(old_disc,3)));
    
    f_color = vec4(red*disc, green*disc, blue*disc, 1.0);
}