#version 330 core

uniform sampler2D tex;
uniform vec4 chosen_button;
uniform float transposition_shader_multiplayer;

in vec2 uvs;
out vec4 f_color;

const vec2 SCREEN_SIZE = vec2(640.0, 360.0);

float glowing_rectangle(vec2 pos, vec4 rect) {
    float coloring = 0.1;

    if (pos.x >= rect.x && pos.x <= rect.x + rect.z &&
        pos.y >= rect.y && pos.y <= rect.y + rect.w) {
        coloring = 1.0;  // Darken the color inside the rectangle
    }

    return coloring;
}

void main() {
    vec4 base_color = texture(tex, uvs);

    // Apply glowing rectangle effects
    float glow_intensity1 = glowing_rectangle(uvs, chosen_button);



    float adjusted_multiplayer = abs(transposition_shader_multiplayer);
    f_color = vec4(base_color.rgb*adjusted_multiplayer*glow_intensity1, 1.0);
}
