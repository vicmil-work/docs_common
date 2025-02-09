# Contains documentation for how to do some things using the standard library

Everything should be supported in C++11 and newer versions across most major platforms(Windows, Linux, Browser using emscripten)

You can either just copy the parts that you find interesting, or download the following:

- [util_std.hpp](../static/util_std.hpp){:download="util_std.hpp"}
- [cpp_build.py](../static/cpp_build.py){:download="cpp_build.py"}
- [util_std_example.cpp](../static/util_std_example.cpp){:download="util_std_example.cpp"}
- [cpp_build_example.py](../static/cpp_build_example.py){:download="cpp_build_example.py"}


### Setting up a c++ compiler on windows
You can download mingw64 on windows using the following tutorial:
https://code.visualstudio.com/docs/cpp/config-mingw

And if you are using powershell, you can just add it to the current path
```
$env:Path = "C:\msys64\ucrt64\bin;" + $env:Path
```

Or add at to your global path by heading to 
settings -> system -> about -> advanced system settings -> environment variables -> system variables -> Path -> edit -> New

If you downloaded mingw using some other method, you may also want to install the following if there is problems with threads:
[https://github.com/meganz/mingw-std-threads](https://github.com/meganz/mingw-std-threads) - enable threading for mingw if it is missing threading support

### Setting up c++ compiler on linux
For linux, the setup is rather trivial. just run the following commands:
```
sudo apt install build-essential
```

### Setting up c++ compiler for targetting the web
Just install emscripten using the following tutorial:
https://emscripten.org/docs/getting_started/downloads.html

### Cross-platform headers

```C++
/**
 * These are a list of **most** cross-platform c++11 headers
*/
#pragma once
#include <iostream>     // For cout, cin and in other ways interracting with the terminal
#include <fstream>
#include <sstream>
#include <filesystem>   // For reading and writing files

#include <string>       // Contains std::string
#include <set>          // Contains std::set
#include <map>          // contains std::map
#include <vector>       // Contains std::vector
#include <list>         // Contains std::list

#include <math.h>       // Includes basic math operations such as sinus, cosinus etc.
#include <cassert>      // For assering values during runtime
#include <regex>        // Includes functions for regex
#include <chrono>       // Includes functions related to time 
#ifdef __MINGW64__      // For supporting multi-thread applications on windows when compiling using mingw
#include "mingw-std-threads/mingw.thread.h"
#else
#include <thread>       // Includes functions for handling multi-thread applications
#endif
#include <complex.h>    // For supporting complex number operations

#include <typeindex>    // For getting the index of different types, and other type information
#include <random>       // For generating random numbers

#ifdef __EMSCRIPTEN__
#include "emscripten.h" // Include emscripten if available, needed to set the main loop function in case of emscripten
#endif

#ifdef __unix__                             /* __unix__ is usually defined by compilers targeting Unix systems */
    #define OS_Linux
#elif defined(_WIN32) || defined(WIN32)     /* _Win32 is usually defined by compilers targeting 32 or   64 bit Windows systems */
    #define OS_Windows
#endif
```

### Automatic tests in c++

```C++
typedef void (*void_function_type)();

typedef std::map<std::string, struct TestClass*> __test_map_type__;
static __test_map_type__* __test_map__ = nullptr;

struct TestClass {
    std::string _id_long;
    virtual void test() {}
    virtual ~TestClass() {}
    TestClass(std::string id, std::string id_long) {
        if ( !__test_map__ ) {
            __test_map__ = new __test_map_type__();
        }
        (*__test_map__)[id] = this;
        _id_long = id_long;
    }
    static void run_all_tests(std::vector<std::string> test_keywords = {}) {
        if(!__test_map__) {
            std::cout << "No tests detected!" << std::endl;
            return;
        }
        __test_map_type__::iterator it = __test_map__->begin();
        while(it != __test_map__->end()) {
            std::pair<const std::string, TestClass*> val = *it;
            it++;
            std::string test_name = val.first;
            std::cout << "<<<<<<< run test: " << test_name << ">>>>>>>";
                try {
                    val.second->test();
                }
                catch (const std::exception& e) {
                    std::cout << "caught error" << std::endl;
                    std::cout << e.what(); // information from error printed
                    exit(1);
                }
                catch(...) {
                    std::cout << "caught unknown error" << std::endl;
                    exit(1);
                } 
            std::cout << "test passed!" << std::endl;
        }
        std::cout << "All tests passed!" << std::endl;
    }
};

#define TestWrapper(test_name, func) \
namespace test_class { \
    struct test_name : vicmil::TestClass { \
        test_name() : vicmil::TestClass(LINE_INFO.to_string_with_func_name(), LINE_INFO.to_long_string()) {} \
        func \
    }; \
} \
namespace test_factory { \
    test_class::test_name test_name = test_class::test_name(); \
}

/**
 * Add a test to be executed
*/
#define AddTest(test_name) \
TestWrapper(test_name ## _, \
void test() { \
    test_name(); \
} \
);
```

```C++
void add_(int x, int y) {
    return x + y;
}

// Add a test for the function
void TEST_add_() {
    assert(add_(1, 2) == 3);
}
AddTest(TEST_add_);

// Run all tests
int main() {
    vicmil::TestClass::run_all_tests();
    return 0;
}
```

### Vector to string

```C++
/*
Convert a vector of something into a string
example: "{123.321, 314.0, 42.0}"
*/
template<class T>
std::string vec_to_str(const std::vector<T>& vec) {
    std::string out_str;
    out_str += "{ ";
    for(int i = 0; i < vec.size(); i++) {
        if(i != 0) {
            out_str += ", ";
        }
        out_str += std::to_string(vec[i]);
    }
    out_str += " }";
    return out_str;
}

/*
Convert a vector of strings into a single string
["a", "b"] -> "{'a', 'b'}"
*/
std::string vec_to_str(const std::vector<std::string>& vec) {
    std::string return_str = "{";
    for(int i = 0; i < vec.size(); i++) {
        if(i != 0) {
            return_str += ", ";
        }
        return_str += "'" + vec[i] + "'";
    }
    return_str += " }";
    return return_str;
}
```

### Convert to binary

```C++
/**
 * Takes an arbitrary type and converts it to binary, eg string of 1:s and 0:es
*/
template<class T>
std::string to_binary_str(T& value) {
    int size_in_bytes = sizeof(T);
    char* bytes = (char*)&value;
    std::string return_str;
    for(int i = 0; i < size_in_bytes; i++) {
        if(i != 0) {
            return_str += " ";
        }
        for(int j = 0; j < 8; j++) {
            if((bytes[i] & (1<<j)) == 0) {
                return_str += "0";
            }
            else {
                return_str += "1";
            }
        }
    }
    return return_str;
}
```

### String replace

```C++
/**
 * Replaces each instance of a str_from to str_to inside str
 * @param str the main string
 * @param str_from the pattern string we would like to replace
 * @param str_to what we want to replace str_from with
*/
inline std::string string_replace(const std::string& str, const std::string& str_from, const std::string& str_to) {
    std::string remaining_string = str;
    std::string new_string = "";
    while(true) {
        auto next_occurence = remaining_string.find(str_from);
        if(next_occurence == std::string::npos) {
            return new_string + remaining_string;
        }
        new_string = new_string + remaining_string.substr(0, next_occurence) + str_to;
        remaining_string = remaining_string.substr(next_occurence + str_from.size(), std::string::npos);
    }
}
```

### Regex find all

```C++
std::vector<std::string> regex_find_all(std::string str, std::string regex_expr) {
    // Wrap regular expression in c++ type
    std::regex r = std::regex(regex_expr);

    // Iterate to find all matches of regex expression
    std::vector<std::string> tokens = std::vector<std::string>();
    for(std::sregex_iterator i = std::sregex_iterator(str.begin(), str.end(), r);
                            i != std::sregex_iterator();
                            ++i )
    {
        std::smatch m = *i;
        //std::cout << m.str() << " at position " << m.position() << '\n';
        tokens.push_back(m.str());
    }
    return tokens;
}
```

### Regex match

```C++
bool regex_match_expr(std::string str, std::string regex_expr) {
    return std::regex_match(str, std::regex(regex_expr));
}
```

### Cut of string after find

```C++
inline std::string cut_off_after_find(std::string str, std::string delimiter) {
    // Find first occurrence
    size_t found_index = str.find(delimiter);

    // Take substring before first occurance
    if(found_index != std::string::npos) {
        return str.substr(0, found_index);
    }
    return str;
}

inline std::string cut_off_after_rfind(std::string str, std::string delimiter) {
    // Find first occurrence
    size_t found_index = str.rfind(delimiter);

    // Take substring before first occurance
    if(found_index != std::string::npos) {
        return str.substr(0, found_index);
    }
    return str;
}
```

### UTF8 support

```C++
/** UTF8 is compatible with ascii, and can be stored in a string(of chars)
 * Since ascii is only 7 bytes, we can have one bit represent if it is a regular ascii
 *  or if it is a unicode character. Unicode characters can be one, two, three or four bytes
 * 
 * See https://en.wikipedia.org/wiki/UTF-8 for more info
**/ 
bool is_utf8_ascii_char(char char_) {
    return ((char)(1<<7) & char_) == 0;
}

// Function to convert UTF-8 to a vector of integers representing Unicode code points
std::vector<int> utf8ToUnicodeCodePoints(const std::string& utf8String) {
    std::vector<int> codePoints;
    size_t i = 0;
    while (i < utf8String.size()) {
        unsigned char c = utf8String[i++];
        int codePoint;
        if ((c & 0x80) == 0) {
            codePoint = c;
        } else if ((c & 0xE0) == 0xC0) {
            codePoint = ((c & 0x1F) << 6);
            codePoint |= (utf8String[i++] & 0x3F);
        } else if ((c & 0xF0) == 0xE0) {
            codePoint = ((c & 0x0F) << 12);
            codePoint |= ((utf8String[i++] & 0x3F) << 6);
            codePoint |= (utf8String[i++] & 0x3F);
        } else if ((c & 0xF8) == 0xF0) {
            codePoint = ((c & 0x07) << 18);
            codePoint |= ((utf8String[i++] & 0x3F) << 12);
            codePoint |= ((utf8String[i++] & 0x3F) << 6);
            codePoint |= (utf8String[i++] & 0x3F);
        }
        codePoints.push_back(codePoint);
    }
    return codePoints;
}
```

```C++
void TEST_utf8ToUnicodeCodePoints() {
    std::string utf8Text = u8"こんにちはtest"; // UTF-8 text
    std::vector<int> codePoints = utf8ToUnicodeCodePoints(utf8Text); // Convert UTF-8 to Unicode code points
    Assert(codePoints[0] == 12371); // Unicode character for 'こ'
    Assert(codePoints[5] == 't') // Unicode/ASCII character for 't'
    Assert(codePoints.size() == 9);
}
```

### Read file contents

```C++
/**
 * Read all the contents of a file and return it as a string
*/
std::string read_file_contents(const std::string& filename) {
    std::ifstream file(filename);
    std::string contents;

    if (file.is_open()) {
        // Read the file content into the 'contents' string.
        std::string line;
        while (std::getline(file, line)) {
            contents += line + "\n"; // Add each line to the contents with a newline.
        }
        file.close();
    } else {
        std::cerr << "Error: Unable to open file " << filename << std::endl;
    }

    return contents;
}

```

### Read file contents line by line

```C++
/**
 * Read all file contents line by line, and return it as a vector where each index represents a line
*/
std::vector<std::string> read_file_contents_line_by_line(const std::string& filename) {
    std::ifstream file(filename);
    std::vector<std::string> contents;

    if (file.is_open()) {
        // Read the file content into the 'contents' string.
        std::string line;
        while (std::getline(file, line)) {
            contents.push_back(line); // Add each line to the contents with a newline.
        }
        file.close();
    } else {
        std::cerr << "Error: Unable to open file " << filename << std::endl;
    }

    return contents;
}

```

### FileManager for reading and writing files

```C++
/**
 * General file manager for easy file management
 * - Contains a lot of utility functions to make your life easier
*/
class FileManager {
    std::string filename;
public:
    std::fstream file; // Read & Write
    //std::ifstream file; // Read only
    //std::ofstream file; // Write only
    FileManager(std::string filename_, bool create_file=false) { // class constructor
        filename = filename_;
        if(create_file) {
            file = std::fstream(filename, std::ios::app | std::ios::binary);
        }
        else {
            file = std::fstream(filename, std::ios::in | std::ios::binary | std::ios::out);
        }
  
        if(!file_is_open()) {
            std::cout << "file could not open!" << std::endl;
            std::cout << filename << std::endl;
            throw;
        }
        else {
            //std::cout << "file opened successfully" << std::endl;
        }
        }
    bool file_is_open() {
        return file.is_open();
    }

    void set_read_write_position(unsigned int index) {
        file.seekg(index);
    }
    unsigned int get_read_write_position() {
        // get current read position
        std::streampos read_pos = file.tellg();
        return read_pos;
    }

    std::vector<char> read_bytes(unsigned int read_size_in_bytes) { // read bytes as binary and write into &output
        std::vector<char> output = std::vector<char>();
        output.resize(read_size_in_bytes);
        file.read(&output[0], read_size_in_bytes); // read this many bytes from read_write_position in file, to &output[0] in memory.
        return output;
    }
    std::vector<char> read_entire_file() {
        unsigned int file_size = get_file_size();
        set_read_write_position(0);
        return read_bytes(file_size);
    }
    void write_bytes(const unsigned char* data, int size_in_bytes) {
        file.write((char*)(void*)data, size_in_bytes);
    }
    void write_bytes(const std::vector<char>& input) {
        file.write(&input[0], input.size());
        // write this many bytes from &input[0] in memory, to read_write_position in file.
        // also increments read_write_position by the same amount of bytes.
    }
    void write_bytes(const std::vector<unsigned char>& input) {
        write_bytes(&input[0], input.size());
    }

    std::string read_str(unsigned int read_size_in_bytes) {
        std::string output = std::string();
        output.resize(read_size_in_bytes);
        file.read(&output[0], read_size_in_bytes);
        return output;
    }
    void write_str(std::string& str) {
        file.write(&str[0], str.length());
    }

    void write_int32(int val) {
        int* val_pointer = &val;
        char* char_pointer = reinterpret_cast<char*>(val_pointer); // convert int* to char* without changing position
        std::vector<char> bytes = {char_pointer[0], char_pointer[1], char_pointer[2], char_pointer[3]};
        write_bytes(bytes);
    }
    int read_int32() {
        std::vector<char> bytes = read_bytes(4);
        char* char_pointer = &bytes[0];
        int* val_pointer = reinterpret_cast<int*>(char_pointer);
        return *val_pointer;
    }

    unsigned int read_uint32() {
        std::vector<char> bytes = read_bytes(4);
        char* char_pointer = &bytes[0];
        unsigned int* val_pointer = reinterpret_cast<unsigned int*>(char_pointer);
        return *val_pointer;
    }

    unsigned char read_uint8() {
        std::vector<char> bytes = read_bytes(1);
        char* char_pointer = &bytes[0];
        unsigned char* val_pointer = reinterpret_cast<unsigned char*>(char_pointer);
        return *val_pointer;
    }

    char read_int8() {
        std::vector<char> bytes = read_bytes(1);
        char* char_pointer = &bytes[0];
        char* val_pointer = reinterpret_cast<char*>(char_pointer);
        return *val_pointer;
    }

    std::string read_word() {
        std::string output = std::string();
        file >> output;
        return output;
    }
    std::string read_next_line() {
        std::string output = std::string();
        std::getline(file, output, '\n');
        return output;
    }
    bool end_of_file() {
        return file.eof();
    }
    void erase_file_contents() {
        file.close();
        file.open(filename, std::ios::trunc | std::ios::out | std::ios::in | std::ios::binary);
        if(!file_is_open()) {
            std::cout << "file could not open!" << std::endl;
            throw;
        }
        else {
            //std::cout << "file opened successfully" << std::endl;
        }
    }
    // NOTE! This will move the read/write position
    unsigned int get_file_size() {
        file.seekg( 0, std::ios::end );
        return get_read_write_position();
    }
};
```

### Get time since epoch

```C++
/**
 * Returns the time since epoch in seconds, 
 * NOTE! Different behaviour on different devices
 * on some devices epoch refers to January 1: 1970, 
 * on other devices epoch might refer to time since last boot
*/
double get_time_since_epoch_s() {
    using namespace std::chrono;
    auto time = duration_cast<nanoseconds>(high_resolution_clock::now().time_since_epoch());
    double nano_secs = time.count();
    return nano_secs / (1000.0 * 1000.0 * 1000.0);
}
double get_time_since_epoch_ms() {
    return get_time_since_epoch_s() * 1000;
}
```

### Sleep

```C++
void sleep_s(double sleep_time_s) {
    double time_ms = sleep_time_s * 1000;
    std::this_thread::sleep_for(std::chrono::milliseconds((int64_t)time_ms));
}
```

```C++
void TEST_sleep() {
    double start_time = get_time_since_epoch_s();
    sleep_s(0.7);
    double end_time = get_time_since_epoch_s();
    double duration = end_time - start_time;
    AssertEq(duration, 0.7, 0.1);
}
```

### PI

```C++
const double PI  = 3.141592653589793238463;
```

### Is power of 2

```C++
inline bool is_power_of_two(unsigned int x) {
    return !(x == 0) && !(x & (x - 1));
}
inline bool is_power_of_two(int x) {
    return !(x == 0) && !(x & (x - 1));
}
```

### Upper power of 2

```C++
unsigned int upper_power_of_two(unsigned int x) {
    int power = 1;
    while(power < x) {
        power*=2;
    }
    return power;
}
```

### Modulo

```C++
double modulo(double val, double mod) {
    if(val > 0) {
        return val - ((int)(val / mod)) * mod;
    }
    else {
        return val - ((int)((val-0.0000001) / mod) - 1) * mod;
    }
}
```

### Degrees radians conversion

```C++
double degrees_to_radians(const double deg) {
    const double PI  = 3.141592653589793238463;
    return deg * 2.0 * PI / 360.0;
}

double radians_to_degrees(const double rad) {
    const double PI  = 3.141592653589793238463;
    return rad * 360.0 / (PI * 2.0);
}
```

### In range

```C++
/**
 * Determine if a value is in range
 * Returns true if min_v <= v <= max_v
*/
template<class T>
inline bool in_range(T v, T min_v, T max_v) {
    if(v < min_v) {
        return false;
    }
    if(v > max_v) {
        return false;
    }
    return true;
}
```

### Vector operations

```C++
/**
 * Determine if a value exists somewhere in a vector
 * @param val The value to look for
 * @param vec The vector to look in
 * @return Returns true if value is somewhere in vector, otherwise returns false
*/
template<class T>
bool in_vector(T val, std::vector<T>& vec) {
    for(int i = 0; i < vec.size(); i++) {
        if(val == vec[i]) {
            return true;
        }
    }
    return false;
}

double get_min_in_vector(std::vector<double> vec) {
    double min_val = vec[0];
    for(int i = 0; i < vec.size(); i++) {
        if(vec[i] < min_val) {
            min_val = vec[i];
        }
    }
    return min_val;
}

double get_max_in_vector(std::vector<double> vec) {
    double max_val = vec[0];
    for(int i = 0; i < vec.size(); i++) {
        if(vec[i] > max_val) {
            max_val = vec[i];
        }
    }
    return max_val;
}

template <class T>
T vec_sum(const std::vector<T>& vec, T zero_element) {
    T sum = zero_element;
    for(int i = 0; i < vec.size(); i++) {
        sum += vec[i];
    }
    return sum;
}

template <class T>
T vec_sum(const std::vector<T>& vec) {
    return vec_sum(vec, (T)0);
}

template <class T>
void vec_sort_ascend(std::vector<T>& vec) {
    std::sort(vec.begin(), 
        vec.end(), 
        [](const T& lhs, const T& rhs) {
            return lhs < rhs;
    });
}

template <class T>
void vec_sort_descend(std::vector<T>& vec) {
    std::sort(vec.begin(), 
        vec.end(), 
        [](const T& lhs, const T& rhs) {
            return lhs > rhs;
    });
}

template <class T>
std::vector<std::pair<T, int>> vec_to_pair_with_indecies(const std::vector<T>& vec) {
    std::vector<std::pair<T, int>> return_vec = {};
    for(int i = 0; i < vec.size(); i++) {
        std::pair<T, int> pair_;
        pair_.first = vec[i];
        pair_.second = i;
        return_vec.push_back(pair_);
    }
    return return_vec;
}
template <class T>
std::vector<std::pair<T, int>> vec_sort_ascend_and_get_indecies(const std::vector<T>& vec) {
    std::vector<std::pair<T, int>> return_vec = vec_to_pair_with_indecies(vec);
    std::sort(return_vec.begin(), 
        return_vec.end(), 
        [](const std::pair<T, int>& lhs, const std::pair<T, int>& rhs) {
            return lhs.first < rhs.first;
    });
    return return_vec;
}
template <class T>
std::vector<std::pair<T, int>> vec_sort_descend_and_get_indecies(const std::vector<T>& vec) {
    std::vector<std::pair<T, int>> return_vec = vec_to_pair_with_indecies(vec);
    std::sort(return_vec.begin(), 
        return_vec.end(), 
        [](const std::pair<T, int>& lhs, const std::pair<T, int>& rhs) {
            return lhs.first > rhs.first;
    });
    return return_vec;
}

template <class T>
void vec_remove(std::vector<T>& vec, std::size_t pos)
{
    auto it = vec.begin();
    std::advance(it, pos);
    vec.erase(it);
}

/**
Extend one vector with another(can also be referred to as vector adding or concatenation)
extend_vec({1, 2}, {3, 4, 5}) -> {1, 2, 3, 4, 5}
@arg vec: the first vector
@arg add_vec: the vector to add to vec
*/
template <class T>
void vec_extend(std::vector<T>& vec, const std::vector<T>& vec_add){
    vec.insert(vec.end(), vec_add.begin(), vec_add.end());
}

/**
Extend one vector with another(can also be referred to as vector adding or concatenation)
extend_vec({1, 2}, {3, 4, 5}) -> {1, 2, 3, 4, 5}
@arg vec: the first vector
@arg add_vec: the vector to add to vec
*/
template <class T>
void vec_insert(std::vector<T>& vec,int index, T val){
    vec.insert(vec.begin()+index, val);
}
```

### Emscripten support

```C++
// Some functions to make working with emscripten easier, should also work without emscripten to make it cross platform
static vicmil::void_function_type update_func_ptr = nullptr;
static vicmil::void_function_type init_func_ptr = nullptr;
void main_app_update() {
    static bool inited = false;
    if(!inited) {
        inited = true;
        if(init_func_ptr != nullptr) {
            init_func_ptr();
        }
    }
    if(update_func_ptr != nullptr) {
        update_func_ptr();
    }
}
void set_app_update(vicmil::void_function_type func_ptr_) {
    update_func_ptr = func_ptr_;
}
void set_app_init(vicmil::void_function_type func_ptr_) {
    init_func_ptr = func_ptr_;
}
void app_start() {
    #ifdef EMSCRIPTEN
        emscripten_set_main_loop(main_app_update, 0, 1);
    #else
        while(true) {
            main_app_update();
        }
    #endif
}
```

```C++
// Example usage
void init() { 
    // do init stuff here, will be called once at the start of the program
    std::cout << "init" << std::endl;
} 
void update() {
    // do update stuff here, will be called continously
    std::cout << "update" << std::endl;
} 

// This makes it work cross platform with emscripten compiler, if compiling for the web
// Stems from the fact that if you do a while loop, the whole browser freezes, so you need to give back 
// control to javascript after each update, which is here done for you automatically :)
int main(int argc, char *argv[]) {
    vicmil::set_app_update(update);
    vicmil::set_app_init(init);
    vicmil::app_start();
    return 0;
}
```

### Typing

```C++
 template <typename T, typename U>
inline bool equals(const std::weak_ptr<T>& t, const std::weak_ptr<U>& u)
{
    return !t.owner_before(u) && !u.owner_before(t);
}

template <typename T, typename U>
inline bool equals(const std::weak_ptr<T>& t, const std::shared_ptr<U>& u)
{
    return !t.owner_before(u) && !u.owner_before(t);
}

template<class T>
std::type_index _get_type_index() {
    return std::type_index(typeid(T));
}
template<class T>
std::string type_to_str() {
    std::type_index typ = _get_type_index<T>();
    std::string name = typ.name();
    return name;
}
template<class T>
int64_t type_to_int() {
    std::type_index typ = _get_type_index<T>();
    std::size_t code = typ.hash_code();
    return (int64_t)code;
}
template<class T>
int64_t type_to_int(T* _) {
    return type_to_int<T>();
}
template<class T>
T* null_if_type_missmatch(T* v, int64_t type_int) {
    if(type_to_int<T>() == type_int) {
        return v;
    }
    return nullptr;
}
```

### Using Python to build C++ projects

NOTE! Implementation not complete: TODO

```python
class BuildSetup:
    def __init__(self, cpp_file_paths: List[str], browser = False):
        # When building c++ projects, this is in general the order the flags should be
        self.n1_compiler_path = get_default_compiler_path(browser = browser)
        self.n2_cpp_files = '"' + '" "'.join(cpp_file_paths) + '"'
        self.n3_optimization_level = ""
        self.n4_macros = ""
        self.n5_additional_compiler_settings = ""
        self.n6_include_paths = ""
        self.n7_library_paths = ""
        self.n8_library_files = ""
        self.n9_output_file = get_default_output_file(browser=browser)

        # If the target platform is the browser
        self.browser_flag = browser

    def include_opengl(self): # Opengl is a cross platform graphics library that also works in the browser(with the right setup)
        add_opengl_flags(self, self.browser_flag)

    def enable_debug(self):
        self.n4_macros += " -D USE_DEBUG"

    def include_asio(self): # Asio is a cross platform networking library to work with sockets etc.
        add_asio_flags(self, browser=self.browser_flag)

    def generate_build_command(self):
        arguments = [
            self.n1_compiler_path, 
            self.n2_cpp_files,
            self.n3_optimization_level,
            self.n4_macros,
            self.n5_additional_compiler_settings,
            self.n6_include_paths,
            self.n7_library_paths,
            self.n8_library_files,
            "-o " + '"' + self.n9_output_file + '"',
        ]
  
        # Reomve arguments with length 0
        arguments = filter(lambda arg: len(arg) > 0, arguments)

        return " ".join(arguments)
  

    def build_and_run(self):
        build_command = self.generate_build_command()

        # Remove the output file if it exists already
        if file_exist(self.n9_output_file):
            delete_file(self.n9_output_file)

        # Run the build command
        print(build_command)
        run_command(build_command)

        invoke_file(self.n9_output_file)


def run_command(command: str) -> None:
    """Run a command in the terminal"""
    platform_name = platform.system()
    if platform_name == "Windows": # Windows
        if command[0] != '"':
            os.system(f'powershell; {command}')
        else:
            os.system(f'powershell; &{command}')
    else:
        os.system(command)
  

def invoke_file(file_path: str):
    if not file_exist(file_path=file_path):
        print(file_path + " does not exist")

    file_extension = file_path.split(".")[-1]

    if file_extension == "html":
        # Create a local python server and open the file in the browser
        launch_html_page(file_path)

    elif file_extension == "exe" or file_extension == "out":
        # Navigate to where the file is located and invoke the file
        file_directory = path_traverse_up(file_path, 0)
        change_active_directory(file_directory)
        run_command('"' + file_path + '"')


# Get the defualt compiler path within vicmil lib
def get_default_compiler_path(browser = False):
    platform_name = platform.system()

    if not browser:
        if platform_name == "Windows": # Windows
            return '"' + path_traverse_up(__file__, 1) + "/deps/win_/mingw64/bin/g++" + '"'
        else:
            return "g++"
  
    else:
        if platform_name == "Windows": # Windows
            return '"' + path_traverse_up(__file__, 1) + "/deps/win_/emsdk/upstream/emscripten/em++.bat" + '"'
        else:
            return '"' + path_traverse_up(__file__, 1) + "/deps/linux_/emsdk/upstream/emscripten/em++" + '"'
  

def add_opengl_flags(build_setup: BuildSetup, browser = False):
    if not browser:
        platform_name = platform.system()

        if platform_name == "Windows": # Windows
            dependencies_directory = path_traverse_up(__file__, 1) + "/deps/win_"

            # SDL
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/include/SDL2" + '"'
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/sdl_mingw/SDL2-2.30.7/x86_64-w64-mingw32/lib" + '"'
      
            # SDL_image
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/sdl_mingw/SDL2_image-2.8.2/x86_64-w64-mingw32/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/sdl_mingw/SDL2_image-2.8.2/x86_64-w64-mingw32/lib" + '"'

            # Glew
            build_setup.n6_include_paths += ' -I"' + dependencies_directory + "/glew-2.2.0/include" + '"'
            build_setup.n7_library_paths += ' -L"' + dependencies_directory + "/glew-2.2.0/lib/Release/x64" + '"'

            build_setup.n8_library_files += ' -l' + "mingw32"
            build_setup.n8_library_files += ' -l' + "glew32"
            build_setup.n8_library_files += ' -l' + "opengl32"
            build_setup.n8_library_files += ' -l' + "SDL2main"
            build_setup.n8_library_files += ' -l' + "SDL2"
            build_setup.n8_library_files += ' -l' + "SDL2_image"

        elif platform_name == "Linux": # Linux
            build_setup.n6_include_paths += ' -I' + "/usr/include"

            build_setup.n8_library_files += ' -l' + "SDL2"
            build_setup.n8_library_files += ' -l' + "SDL2_image"
            build_setup.n8_library_files += ' -l' + "GL"  #(Used for OpenGL on desktops)
            build_setup.n8_library_files += ' -l' + "SDL2_image"

        else:
            raise NotImplementedError()

    else:
        build_setup.n5_additional_compiler_settings += " -s USE_SDL=2"
        build_setup.n5_additional_compiler_settings += " -s USE_SDL_IMAGE=2"
        build_setup.n5_additional_compiler_settings += " -s EXTRA_EXPORTED_RUNTIME_METHODS=ccall,cwrap"
        # build_setup.n5_additional_compiler_settings += """ -s SDL2_IMAGE_FORMATS='["png"]'"""
        build_setup.n5_additional_compiler_settings += " -s FULL_ES3=1"


# Asio is used for sockets and network programming
def add_asio_flags(build_setup: BuildSetup, browser = False):
    if browser:
        raise Exception("Asio is not supported for the browser, consider using websockets bindings to javascript(TODO)")
  
    build_setup.n6_include_paths += ' -I"' + path_traverse_up(__file__, 1) + "/deps/external_libraries/asio/include" + '"'

    platform_name = platform.system()
    if platform_name == "Windows": # Windows
        build_setup.n8_library_files += " -lws2_32" # Needed to make it compile with mingw compiler

    else:
        print("asio include not implemented for ", platform_name)
```
