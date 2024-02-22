#pragma once
#include "../Entity/Entity.h"
#include "../Pch.h"
#include <GL/glew.h>

namespace OverCyde {
    class Component {
        public:
            Component(Entity *entity, uint8_t updateOrder = 0) : m_entity(entity),
                                                                m_updateOrder(updateOrder)
            { this->m_entity->AddComponent(this); }

            Component() {};

            virtual ~Component() { this->m_entity->RemoveComponent(this); }

            virtual void Update(int deltaTime) {};
            uint8_t GetUpdateOrder() const { return this->m_updateOrder; }

        protected:
            Entity* m_entity;
            uint8_t m_updateOrder;
    };
}
