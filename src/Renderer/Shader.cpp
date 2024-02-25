#include "Shader.h"
#include "../Log.h"

namespace Core {
    namespace Debugging {

        static inline bool CheckShader(uint32_t ID) {
            GLint maxLength = 0;
            std::vector<GLchar> buffer(maxLength);

            int parameter;
            glGetShaderiv(ID, GL_INFO_LOG_LENGTH, &parameter);
            if (parameter > 0) {
                buffer.resize(parameter);
                glGetShaderInfoLog(ID, parameter, &maxLength, &buffer[0]);
                LOG_CORE_ERROR("{0}", buffer.data());
                return false;
            }
            return true;
        }

        static inline bool ValidateShaderProgram(uint32_t ID) {
            int result;

            glValidateProgram(ID);
            glGetProgramiv(ID, GL_VALIDATE_STATUS, &result);
            LOG_CORE_INFO("validation of program {0} {0}", ID, result);

            glGetProgramiv(ID, GL_LINK_STATUS, &result);
            LOG_CORE_INFO("linking of program {0} {0}", ID, result);

            glGetProgramiv(ID, GL_ACTIVE_ATTRIBUTES, &result);
            LOG_CORE_INFO("active attribute of program {0} {0}", ID, result);

            glGetProgramiv(ID, GL_ACTIVE_UNIFORMS, &result);
            LOG_CORE_INFO("active uniform  of program {0} {0}", ID, result);

            glGetProgramiv(ID, GL_ACTIVE_UNIFORM_MAX_LENGTH, &result);
            LOG_CORE_INFO("active uniform Max Length of programm {0} {0}", ID, result);

            return result == 1;
        }
    }

    Shader::Shader(const std::string& vertexPath, const std::string& fragmentPath)
    {
        this->CreateShader(this->ReadFile(vertexPath).c_str(), GL_VERTEX_SHADER);
        this->CreateShader(this->ReadFile(fragmentPath).c_str(), GL_FRAGMENT_SHADER);
        this->CreateProgram();

        glDeleteShader(this->m_VertexID);
        glDeleteShader(this->m_FragmentID);
        
        glDetachShader(this->m_ID, this->m_VertexID);
        glDetachShader(this->m_ID, this->m_FragmentID);
    }

    Shader::~Shader() {
        glDeleteProgram(this->m_ID);
    }

    bool Shader::CreateShader(const char* shaderCode, const uint32_t type){
        unsigned int shader;

        switch (type) {
            case GL_VERTEX_SHADER:
                shader = this->m_VertexID = glCreateShader(GL_VERTEX_SHADER);
                break;
            case GL_FRAGMENT_SHADER:
                shader = this->m_FragmentID = glCreateShader(GL_FRAGMENT_SHADER);
                break;
        }

        glShaderSource(shader, 1, &shaderCode, NULL);
        glCompileShader(shader);

        int status;
        glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
        if (!status) {
            Debugging::CheckShader(shader);
            return false;
        }
        return true;
    }

    void Shader::CreateProgram(){
        this->m_ID = glCreateProgram();
        glAttachShader(this->m_ID, this->m_VertexID);
        glAttachShader(this->m_ID, this->m_FragmentID);
        glLinkProgram(this->m_ID);
        Debugging::ValidateShaderProgram(this->m_ID);
    }

    std::string Shader::ReadFile(const std::string &path) {
        std::ifstream file;
        file.exceptions(std::ifstream::failbit | std::ifstream::badbit);
        try{
            file.open(path);
            std::stringstream stream;
            stream << file.rdbuf();
            file.close();
            return stream.str();
        }catch(std::ifstream::failure e){
            LOG_CORE_ERROR("ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ");
        }
    }

    void Shader::Bind() const { 
        glUseProgram(this->m_ID); 
    }

    void Shader::Unbind() const { 
        glUseProgram(0); 
    }
}



