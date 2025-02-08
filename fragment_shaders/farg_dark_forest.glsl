#version 330 core

uniform sampler2D tex;
uniform float transposition_shader_multiplayer;

const vec2 u_resolution = vec2(640.,360.);

in vec2 uvs;
out vec4 f_color;

void main() {
    float adjusted_multiplayer = abs(transposition_shader_multiplayer)/2;
    float aspect = u_resolution.x / u_resolution.y;

    const float RADIUS = 2.;

    vec2 circle_centre = vec2(0.5, 0.7);
    vec2 ellipse_radii = vec2(RADIUS, RADIUS*aspect);  // Control the radii for X and Y directions

    float red = texture(tex, uvs).r;
    float green = texture(tex, uvs).g;
    float blue = texture(tex, uvs).b;

    // Compute distance in normalized coordinates for the ellipse
    vec2 normalized_coords = (uvs - circle_centre) / ellipse_radii;
    float disc = length(normalized_coords);

    disc = 4.0 * disc;

    if (disc > 1.0) {
        disc = 1.0;
    }

    disc = abs(disc - 1.0) * adjusted_multiplayer;
    
    disc = max(0.025,pow(disc, 3));



    f_color = vec4(red * disc, green * disc, blue * disc, 1.0);
}