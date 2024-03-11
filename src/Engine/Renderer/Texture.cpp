#include "Texture.h"
#include "RendererAPI.h"
#include "../OpenGL/OpenGLTexture.h"

namespace Engine {
    Texture2D* Texture2D::Create(std::string& path) {
        switch (RendererAPI::GetAPI()) {
            case RendererAPI::API::None:        LOG_ENGINE_ERROR("API::None doesn't exists");
            case RendererAPI::API::OpenGL:      return new OpenGLTexture2D(path);
        }
        
        ENGINE_ASSERT(false, "API not found!");
        return nullptr;
    }
}