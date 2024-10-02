from fastapi import HTTPException
from sqlalchemy import select, update


class DatabaseMixin:
    @classmethod
    async def get_all(cls, asession):
        res = await asession.execute(select(cls))
        return list(res.scalars())

    @classmethod
    async def create(cls, asession, **kwargs):
        instance = cls(**kwargs)
        try:
            asession.add(instance)
            await asession.commit()
            await asession.refresh(instance)
        except Exception as e:
            await asession.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating record: {str(e)}")
        return instance

    @classmethod
    async def get_element(cls, asession, key: str, value):
        column = getattr(cls, key)
        result = await asession.execute(select(cls).where(column == value))
        return result.scalars().first()

    @classmethod
    async def update_item(cls, asession, key: str, value, **kwargs):
        item = await cls.get_element(asession, key=key, value=value)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)

        try:
            await asession.commit()
            await asession.refresh(item)
        except Exception as e:
            await asession.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

        return item

    @classmethod
    async def get_by_telegram_id(cls, telegram_id: str, asession):
        result = await asession.execute(select(cls).where(cls.telegram_id == telegram_id))
        return result.scalars().first()

    @classmethod
    async def get_by_id(cls, id: int, asession):
        result = await asession.execute(select(cls).where(cls.id == id))
        return result.scalars().first()

    @classmethod
    async def create_user(cls, user_id: int, asession):
        new_user = cls(id=user_id)
        asession.add(new_user)

        try:
            await asession.commit()
            await asession.refresh(new_user)
        except Exception as e:
            await asession.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

        return new_user

    @classmethod
    async def update_user(cls, user_id: int, asession, **kwargs):
        user = await cls.get_by_id(user_id, asession)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        try:
            await asession.commit()
            await asession.refresh(user)
        except Exception as e:
            await asession.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

        return user

    @classmethod
    async def get_elements_by_owner_id(cls, owner_id: int, asession):
        result = await asession.execute(
            select(cls).where(cls.owner_id == owner_id)
        )
        activities = result.scalars().all()
        return activities

    @classmethod
    async def get_data_by_name(cls, name: str, asession):
        result = await asession.execute(select(cls).where(cls.name == name))
        return result.scalars().first()

    async def update(self, key, value, asession) -> None:
        cls = type(self)
        await asession.execute(
            update(cls).where(cls.id == self.id).values({key: value})
        )
        object.__setattr__(self, key, value)
        await asession.commit()
