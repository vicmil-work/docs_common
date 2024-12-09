# Image handling in C++

### Include stb for image handling

```C++
#define STB_IMAGE_WRITE_IMPLEMENTATION
#define STB_IMAGE_IMPLEMENTATION
#include "stb/stb_image.h"
#include "stb/stb_image_write.h"
```

### Image handling in c++

Requires that you have included stb

```C++
struct ColorRGBA_UChar {
    unsigned char r = 0;
    unsigned char g = 0;
    unsigned char b = 0;
    unsigned char a = 0;
    ColorRGBA_UChar(){}
    ColorRGBA_UChar(int r_, int g_, int b_, int a_) {
        r = r_;
        g = g_;
        b = b_;
        a = a_;
    }
    std::string to_string() {
        return vicmil::vec_to_str<int>({r, g, b});
    }
    bool operator==(const ColorRGBA_UChar& other) const {
        return  r == other.r && 
                g == other.g && 
                b == other.b && 
                a == other.a;
    }
}

struct ImageRGBA_UChar {
    int w;
    int h;
    std::vector<ColorRGBA_UChar> pixels;
    void resize(unsigned int new_width, unsigned int new_height) {
        pixels.resize(new_width * new_height)
    }
    ColorRGBA_UChar* get_pixel(int x, int y) {
        return &pixels[y * width + x]
    }
    unsigned char* get_pixel_data() {
        return (unsigned char*)((void*)(&pixels[0]));
    }
    void set_pixel_data(unsigned char* data, int byte_count) {
        assert(byte_count == pixels.size() * sizeof(ColorRGBA_UChar));
        std::memcpy(&pixels[0], data, byte_count);
    }

    static void load_png_from_file(std::string filename, ImageRGBA_UChar& return_image) const {
        // If it failed to load the file, the width will be zero for the returned image object
        int w = 0;
        int h = 0;
        int n = 0;
        int comp = 4; // r, g, b, a
        unsigned char *data = stbi_load(filename.c_str(), &w, &h, &n, comp);
        return_image.resize(w, h);
        if(w != 0) {
            return_image.set_pixel_data(data, w * h * 4);
        }
        stbi_image_free(data);
    }
    void save_as_png(std::string filename) const {
        int comp = 4; // r, g, b, a
        const void *data = get_pixel_data();
        int stride_in_bytes = 0;
        stbi_write_png(filename.c_str(), width, height, comp, data, stride_in_bytes);
    }

    std::vector<unsigned char> to_png_as_bytes(Image<ColorRGBA_UChar>& image) const {
        int comp = 4; // r, g, b, a
        void* data = get_pixel_data();
        int stride_in_bytes = 0;
        stbi_write_func& write_func = _write_to_vector;

        std::unique_ptr<std::vector<unsigned char>> vec = std::make_unique<std::vector<unsigned char>>();
        std::vector<unsigned char>* vec_ptr = vec.get();
        stbi_write_png_to_func(write_func, vec_ptr, width, height, comp, data, stride_in_bytes);
        return *vec;
    }
    static void png_as_bytes_to_image(const unsigned char* bytes, int length, ImageRGBA_UChar& return_image) {
        int w;
        int h;
        int n;
        int comp = 4; // r, g, b, a
      
        unsigned char *data = stbi_load_from_memory(bytes, length, &w, &h, &n, comp);
        return_image.resize(w, h);
        return_image.set_pixel_data(data, w * h * 4);
        stbi_image_free(data);
        return new_image;
    }
    static void png_as_bytes_to_image(const std::vector<unsigned char>& data, ImageRGBA& return_image) {
        return png_as_bytes_to_image(&data[0], data.size(), return_image);
    }
};
```

### Loading fonts in c++

Note! Code is not tested, so it will probably contain some bugs

```C++
#define STB_TRUETYPE_IMPLEMENTATION 
#include "stb/stb_truetype.h"
```

```C++
// For loading true type fonts (.ttf)
struct FontLoader {
    stbtt_fontinfo info;
    std::vector<unsigned char> font_data;

    // Calculated from line height
    int line_height;
    float scale;
    int ascent; // Line spacing in y direction
    int descent;
    int lineGap;

    void load_font_from_memory(unsigned char* fontBuffer_, int size, int line_height_=64) {
        // Load font into buffer
        font_data.resize(size);
        memcpy(&font_data[0], fontBuffer_, size);

        // Prepare font
        if (!stbtt_InitFont(&info, &font_data[0], 0))
        {
            printf("failed\n");
        }
        set_line_height(line_height_); // Set default line height
    }
    void load_font_from_file(std::string filepath, int line_height_=64) {
        vicmil::FileManager file = vicmil::FileManager(filepath);
        std::vector<char> data = file.read_entire_file();
        load_font_from_memory((unsigned char*)&data[0], data.size(), line_height_);
    }

    void set_line_height(int new_line_height) {
        line_height = new_line_height;
        scale = stbtt_ScaleForPixelHeight(&info, line_height);
        int ascent; // Line spacing in y direction
        int descent;
        int lineGap;
        stbtt_GetFontVMetrics(&info, &ascent, &descent, &lineGap);
        ascent = roundf(ascent * scale);
        descent = roundf(descent * scale);
    }

    void _get_character_advancement(const int character, int* advanceWidth, int* leftSideBearing) {
        // Advance width is how much to advance to the right
        // leftSideBearing means that it overlaps a little with the previous character
        stbtt_GetCodepointHMetrics(&info, character, advanceWidth, leftSideBearing);
        *advanceWidth = roundf(*advanceWidth * scale);
        *leftSideBearing = roundf(*leftSideBearing * scale);
    }

    int _get_kernal_advancement(const int character1, const int character2) {
        int kern = stbtt_GetCodepointKernAdvance(&info, character1, character2);
        return roundf(kern * scale);
    }

    RectT<int> _get_character_bounding_box(const int character) {
        int ax;
	    int lsb;
        stbtt_GetCodepointHMetrics(&info, character, &ax, &lsb);

        // Get bounding box for character (may be offset to account for chars that dip above or below the line)
        int c_x1, c_y1, c_x2, c_y2;
        stbtt_GetCodepointBitmapBox(&info, character, scale, scale, &c_x1, &c_y1, &c_x2, &c_y2);
        return RectT<int>(c_x1, c_y1, c_x2 - c_x1, c_y2 - c_y1);
    }

    // Get image of character
    Image<unsigned char> get_character_image(const int character) {
        RectT<int> bounding_box = _get_character_bounding_box(character);
        Image<unsigned char> return_image = Image<unsigned char>();
        return_image.resize(bounding_box.w, bounding_box.h, 127);
        stbtt_MakeCodepointBitmap(&info, (unsigned char*)&return_image.pixels[0], bounding_box.w, bounding_box.h, bounding_box.w, scale, scale, character);
        return return_image;
    }

    Image<ColorRGBA_UChar> get_character_image_rgba(const int character, ColorRGBA_UChar color_mask=ColorRGBA_UChar(255, 255, 255, 255)) {
        Image<unsigned char> character_image = get_character_image(character);
        Image<ColorRGBA_UChar> return_image;
        return_image.resize(character_image.width, character_image.height);
        for(int x = 0; x < character_image.width; x++) {
            for(int y = 0; y < character_image.height; y++) {
                unsigned int pixel_index = character_image.get_pixel_index(x, y);
                int v = character_image.pixels[pixel_index];
                int r = (color_mask.r * v) / 255;
                int g = (color_mask.g * v) / 255;
                int b = (color_mask.b * v) / 255;
                int a = color_mask.a;
                return_image.pixels[pixel_index] = ColorRGBA_UChar(r, g, b, a);
            }
        }
        return return_image;
    }

    // Get where font images in a text should be placed. 
    // Some fonts may take into consideration which letters are next to each other, so-called font kerning
    // Characters are specified in unicode(but normal ascii will be treated as usual)
    std::vector<RectT<int>> get_character_image_positions(const std::vector<int> characters) {
        std::vector<RectT<int>> return_vec = {};
        return_vec.reserve(characters.size());

        int x = 0;
        for(int i = 0; i < characters.size(); i++) {
            // Get bounding box for character
            RectT<int> image_pos = _get_character_bounding_box(characters[i]);
            image_pos.x += x;
            image_pos.y += ascent;

            int advanceWidth;
            int leftSideBearing;
            _get_character_advancement(characters[i], &advanceWidth, &leftSideBearing);
            image_pos.x += leftSideBearing;

            // Push back bounding box
            return_vec.push_back(image_pos);

            // Increment position if there is another letter after
            if(i + 1 != characters.size()) {
                x += advanceWidth;
                x += _get_kernal_advancement(characters[i], characters[i + 1]);
            }
        }
        return return_vec;
    }

    // Get the glyph index of character
    // (Can be used to determine if two letters correspond to the same font image)
    int get_glyph_index(const int character) {
        int glyphIndex = stbtt_FindGlyphIndex(&info, character);
        if (glyphIndex == 0) {
            Debug("Glyph not found for codepoint: " << character);
        }
        return glyphIndex;
    }
    // Determine if a letter/character/unicode character is a part of the loaded font
    bool character_is_part_of_font(const int character) {
        return get_glyph_index(character) != 0;
    }
};
```

```C++
// Example
FontLoader font_loader = FontLoader();
font_loader.load_font_from_file("my_font.ttf")
Image<unsigned char> my_image = font_loader.get_character_image("a");
my_image.to_png_file("letter_a.png");
```
