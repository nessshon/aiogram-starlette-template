from aiogram import Router, F

router = Router()
router.callback_query.filter(F.message.chat.type == "private")
