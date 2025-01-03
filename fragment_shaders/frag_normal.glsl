#version 330 core

uniform sampler2D tex;
uniform float transposition_shader_multiplayer;

in vec2 uvs;
out vec4 f_color;

void main(){
    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(texture(tex, uvs).rgb*adjusted_multiplayer, 1.0);
}