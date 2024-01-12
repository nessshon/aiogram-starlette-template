from aiogram import Router, F

router = Router()
router.inline_query.filter(F.chat_type == "sender")
