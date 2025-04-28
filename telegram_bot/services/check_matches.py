from django.utils import timezone
from matches.models import Match
from bets.models import Bet
from users.models import TelegramUser
from aiogram import Bot
from telegram_bot.config import TELEGRAM_BOT_TOKEN
from telegram_bot.time import format_datetime_ru
from django.db.models import F
from asgiref.sync import sync_to_async
from django.db import transaction
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def check_matches_and_notify():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        now = timezone.now()
        finished_matches = await sync_to_async(list)(
            Match.objects.filter(is_finished=True, notified=False).prefetch_related('bets')
        )
        logger.info(f"Найдено {len(finished_matches)} завершенных матчей для обработки")

        for match in finished_matches:
            bets = await sync_to_async(list)(match.bets.all().select_related('option'))
            logger.info(f"Обработка ставок для матча {match.team1} vs {match.team2}, найдено {len(bets)} ставок")

            for bet in bets:
                try:
                    user = await sync_to_async(lambda: bet.user)()
                    if not user:
                        logger.warning(f"Пользователь для ставки {bet.id} не найден")
                        continue

                    telegram_id = await sync_to_async(lambda: user.telegram_id)()
                    if not telegram_id:
                        logger.warning(f"telegram_id отсутствует для user_id={user.id}")
                        continue

                    bet_option = await sync_to_async(lambda: bet.option.option)()
                    match_winner = await sync_to_async(lambda: match.winner)()

                    is_won = bet_option == match_winner
                    amount = await sync_to_async(lambda: bet.amount)()
                    coefficient = await sync_to_async(lambda: bet.option.get_coefficient())()

                    if coefficient is None:
                        logger.warning(f"Коэффициент не найден для BetOption {bet.option.id}")
                        continue

                    payout = amount * coefficient if is_won else 0

                    await sync_to_async(
                        lambda: transaction.atomic(
                            Bet.objects.filter(id=bet.id).update(
                                is_won=is_won,
                                payout=payout
                            )
                        )
                    )()
                    formatted_time = format_datetime_ru(match.start_time)

                    if is_won:
                        await sync_to_async(
                            lambda: transaction.atomic(
                                TelegramUser.objects.filter(id=user.id).update(
                                    balance=F('balance') + payout
                                )
                            )
                        )()
                        message = (f"🎉Поздравляем ваша ставка сыграла.\n"
                                   f"Вы выиграли на матче: {match.team1} vs {match.team2}!\n"
                                   f"Дата: {formatted_time}.\n"
                                   f"Ваш выигрыш: {payout} 💰")
                    else:
                        message = (f"😢К сожелению ваша ставка не сыграла.\n"
                                   f"Вы проиграли на матче: {match.team1} vs {match.team2}.\n"
                                   f"Дата: {formatted_time}.\n"
                                   f"Желаем удачи в следещем разу🍀")

                    await bot.send_message(chat_id=telegram_id, text=message)
                    logger.info(f"Уведомление отправлено пользователю {telegram_id}")

                except Exception as e:
                    logger.error(f"Ошибка при уведомлении пользователя user_id={getattr(user, 'id', 'unknown')}: {e}")
                    continue

            match.notified = True
            await sync_to_async(match.save)()
            logger.info(f"Матч {match.team1} vs {match.team2} помечен как уведомленный")

    except Exception as e:
        logger.error(f"Ошибка в check_matches_and_notify: {e}")

    finally:
        await bot.session.close()
        logger.info("Сессия бота закрыта")
