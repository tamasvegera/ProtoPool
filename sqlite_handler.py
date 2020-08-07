import sqlite3
from sqlite3 import Error
import time

main_db_file = "./mcc_pool_payments.db"

class Database:
    def __init__(self, db_file):
        sql_create_payments_table = """ CREATE TABLE IF NOT EXISTS payments (
                                        timestamp int NOT NULL,
                                        reward_block int NOT NULL,
                                        from_account int NOT NULL,
                                        to_account int NOT NULL,
                                        amount float NOT NULL,
                                        paid tinyint NOT NULL,
                                        acked_by_wallet tinyint NOT NULL,
                                        confirmed tinyint NOT NULL,
                                        share_rate float NOT NULL,
                                        orphan tinyint NOT NULL
                                    ); """

        self.conn = sqlite3.connect(db_file)
        if self.conn is not None:
            try:
                c = self.conn.cursor()
                c.execute(sql_create_payments_table)
            except Error as e:
                print(e)
        else:
            print("Error! Cannot create the database connection")

    def add_payment_to_DB(self, reward_block, from_account, to_account, share_rate):
        sql = "INSERT INTO payments (timestamp, reward_block, from_account, to_account, amount, paid, acked_by_wallet, confirmed, share_rate, orphan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        payment = (int(time.time()), reward_block, from_account, to_account, 0, False, False, False, share_rate, False)

        c = self.conn.cursor()
        c.execute(sql, payment)
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def set_amount_for_payment(self, reward_block, from_account, to_account, new_amount):
        sql = "UPDATE payments SET amount = ? WHERE reward_block = ? AND from_account = ? AND to_account = ?"
        payment = (new_amount, reward_block, from_account, to_account)
        c = self.conn.cursor()
        c.execute(sql, payment)
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def set_payment_to_paid(self, reward_block, from_account, to_account):
        sql = "UPDATE payments SET paid = TRUE WHERE reward_block = ? AND from_account = ? AND to_account = ?"
        payment = (reward_block, from_account, to_account)
        c = self.conn.cursor()
        c.execute(sql, payment)
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def set_block_to_acked_by_wallet(self, reward_block):
        sql = "UPDATE payments SET acked_by_wallet = TRUE WHERE reward_block = ?"
        c = self.conn.cursor()
        c.execute(sql, (reward_block,))
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def set_block_confirmed(self, reward_block):
        sql = "UPDATE payments SET confirmed = TRUE WHERE reward_block = %s"
        c = self.conn.cursor()
        c.execute(sql, (reward_block,))
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def set_block_to_orphan(self, block):
        sql = "UPDATE payments SET orphan = TRUE WHERE reward_block = %s"
        c = self.conn.cursor()
        c.execute(sql, (block,))
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def delete_zero_txs(self):
        sql = "DELETE FROM payments WHERE amount = 0  AND share_rate=0 AND acked_by_wallet = TRUE"
        c = self.conn.cursor()
        c.execute(sql)
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def remove_payment_from_DB(self, from_account, to_account):
        sql = "DELETE FROM payments WHERE from_account = %s AND to_account = ?"
        payment = (from_account, to_account)
        c = self.conn.cursor()
        c.execute(sql, payment)
        try:
            self.conn.commit()
        except sqlite3.DatabaseError:
            self.conn.rollback()

    def get_payments_of_block(self, block):
        sql = "SELECT * FROM payments WHERE reward_block = ?"
        payment = (block,)
        c = self.conn.cursor()
        c.execute(sql, payment)

        return c.fetchall()

    def get_unacked_blocks(self):
        sql = "SELECT * FROM payments WHERE acked_by_wallet = FALSE AND orphan = FALSE"
        c = self.conn.cursor()
        c.execute(sql)

        return c.fetchall()

    def get_unconfirmed_blocks(self):
        sql = "SELECT * FROM payments WHERE acked_by_wallet = TRUE AND confirmed = FALSE AND orphan = FALSE"
        c = self.conn.cursor()
        c.execute(sql)

        return c.fetchall()

    def get_unpaid_payments(self):
        sql = "SELECT * FROM payments WHERE paid = FALSE AND acked_by_wallet = TRUE AND confirmed = TRUE AND orphan = FALSE"
        c = self.conn.cursor()
        c.execute(sql)

        return c.fetchall()

    def is_block_in_db_already(self, block):
        sql = "SELECT * FROM payments WHERE reward_block = ?"
        c = self.conn.cursor()
        c.execute(sql, (block,))

        result = c.fetchall()
        if len(result):
            return True
        else:
            return False

db = Database(main_db_file)