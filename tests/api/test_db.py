from datetime import datetime
from venv import logger

import pytest
from sqlalchemy.orm import Session

from models.db_tests_models.account_transaction_template_model import AccountTransactionTemplate
from models.db_tests_models.movies_template_model import Movies
from utils.data_generator import DataGenerator

class TestsDB:
    def transfer_money(self, session, from_account, to_account, amount):
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

        print(vars(to_account))

        try:
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                session.commit()
            else:
                raise ValueError("Недостаточно средств на счете.")
        except ValueError:
            raise ValueError("Недостаточно средств на счете.")


    def test_accounts_transaction_template_positive(self, db_session: Session):
        jack_initial_balance = 8000
        troy_initial_balance = 5000
        transfer_sum = 3000

        jack = AccountTransactionTemplate(user=f"Jack_{DataGenerator.generate_random_int()}", balance=jack_initial_balance)
        troy = AccountTransactionTemplate(user=f"Troy_{DataGenerator.generate_random_int()}", balance=troy_initial_balance)

        db_session.add_all([jack, troy])
        db_session.commit()

        assert jack.balance == jack_initial_balance
        assert troy.balance == troy_initial_balance

        try:
            self.transfer_money(db_session, from_account=jack.user, to_account=troy.user, amount=transfer_sum)
            assert jack.balance == jack_initial_balance - transfer_sum
            assert troy.balance == troy_initial_balance + transfer_sum
        except ValueError as ve:
            assert jack.balance == jack_initial_balance
            assert troy.balance == troy_initial_balance
            pytest.fail(f'Ошибка выполнения метода transfer_money - {ve}')
        except Exception as e:
            db_session.rollback()
            assert jack.balance == jack_initial_balance
            assert troy.balance == troy_initial_balance
            pytest.fail(f'Возникла ошибка - {e}')
        finally:
            db_session.delete(jack)
            db_session.delete(troy)
            db_session.commit()

            assert db_session.query(AccountTransactionTemplate).filter_by(user=jack.user).count() == 0
            assert db_session.query(AccountTransactionTemplate).filter_by(user=troy.user).count() == 0


    def test_accounts_transaction_template_negative(self, db_session: Session):
        jack_initial_balance = 8000
        troy_initial_balance = 5000
        transfer_sum = 10000

        jack = AccountTransactionTemplate(user=f"Jack_{DataGenerator.generate_random_int()}", balance=jack_initial_balance)
        troy = AccountTransactionTemplate(user=f"Troy_{DataGenerator.generate_random_int()}", balance=troy_initial_balance)

        db_session.add_all([jack, troy])
        db_session.commit()

        assert jack.balance == jack_initial_balance
        assert troy.balance == troy_initial_balance

        try:
            self.transfer_money(db_session, from_account=jack.user, to_account=troy.user, amount=transfer_sum)
        except ValueError as ve:
            logger.info(f'Ошибка выполнения метода transfer_money - {ve}')

            assert jack.balance == jack_initial_balance
            assert troy.balance == troy_initial_balance

            db_session.delete(jack)
            db_session.delete(troy)
            db_session.commit()
        except Exception as e:
            db_session.rollback()

            assert jack.balance == jack_initial_balance
            assert troy.balance == troy_initial_balance

            db_session.delete(jack)
            db_session.delete(troy)
            db_session.commit()

            pytest.fail(f'Возникла ошибка - {e}')
        finally:
            assert db_session.query(AccountTransactionTemplate).filter_by(user=jack.user).count() == 0
            assert db_session.query(AccountTransactionTemplate).filter_by(user=troy.user).count() == 0


    def test_user_delete(self, db_session: Session):
        movie = Movies(
            id = 123456,
            name= 'TestMovie',
            price = 260,
            description = 'avawa',
            image_url = 'asdasd',
            location = 'MSK',
            published = True,
            rating = 6,
            genre_id = 10,
            created_at = datetime.now()
        )

        db_session.add(movie)
        db_session.commit()

        movie_in_db = db_session.query(Movies).filter_by(id=movie.id)

        assert movie_in_db.count() == 1

        db_session.delete(movie)
        db_session.commit()

        assert movie_in_db.count() == 0
