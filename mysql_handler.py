import mysql.connector, time

db_name = "ProtoPool"
payments_table_name = "protopoolpayments_v3"

poolDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "anyadpicsaja",
    database = db_name
)

poolCursor = poolDB.cursor(buffered=True)
mysql_busy = False
retry = 5

def add_payment_to_DB(reward_block, from_account, to_account, share_rate):
    global payments_table_name, mysql_busy
    sql = "INSERT INTO " + payments_table_name + " (timestamp, reward_block, from_account, to_account, amount, paid, acked_by_wallet, confirmed, share_rate, orphan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    payment = (int(time.time()), reward_block, from_account, to_account, 0, False, False, False, share_rate, False)
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, payment)
    poolDB.commit()
    mysql_busy = False

def set_amount_for_payment(reward_block, from_account, to_account, new_amount):
    global mysql_busy
    #print("Setting to paid, " + str(reward_block) + ' ' + str(from_account) + ' ' + str(to_account))
    sql = "UPDATE " + payments_table_name + " SET amount = %s WHERE reward_block = %s AND from_account = %s AND to_account = %s"
    payment = (new_amount, reward_block, from_account, to_account)
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, payment)
    poolDB.commit()
    mysql_busy = False

def set_payment_to_paid(reward_block, from_account, to_account):
    global mysql_busy
    #print("Setting to paid, " + str(reward_block) + ' ' + str(from_account) + ' ' + str(to_account))
    sql = "UPDATE " + payments_table_name + " SET paid = TRUE WHERE reward_block = %s AND from_account = %s AND to_account = %s"
    payment = (reward_block, from_account, to_account)
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, payment)
    poolDB.commit()
    mysql_busy = False

def set_block_to_acked_by_wallet(reward_block):
    global mysql_busy
    sql = "UPDATE " + payments_table_name + " SET acked_by_wallet = TRUE WHERE reward_block = %s"

    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (reward_block,))
    poolDB.commit()
    mysql_busy = False

def set_block_confirmed(reward_block):
    global mysql_busy
    sql = "UPDATE " + payments_table_name + " SET confirmed = TRUE WHERE reward_block = %s"

    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (reward_block,))
    poolDB.commit()
    mysql_busy = False

def set_block_to_orphan(block):
    global mysql_busy
    sql = "UPDATE " + payments_table_name + " SET orphan = TRUE WHERE reward_block = %s"

    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (block,))
    poolDB.commit()
    mysql_busy = False

def delete_zero_txs():
    global mysql_busy
    sql = "DELETE FROM " + payments_table_name + " WHERE amount = 0  AND share_rate=0 AND acked_by_wallet = TRUE"

    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql)
    poolDB.commit()
    mysql_busy = False

def remove_payment_from_DB(from_account, to_account):
    global mysql_busy
    sql = "DELETE FROM " + payments_table_name + " WHERE from_account = %s AND to_account = %s"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (from_account, to_account,))
    poolDB.commit()
    mysql_busy = False

def get_payments_of_block(block):
    global mysql_busy

    sql = "SELECT * FROM " + payments_table_name + " WHERE reward_block = %s"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (block,))
    mysql_busy = False
    return poolCursor.fetchall()

def get_unacked_blocks():
    global mysql_busy

    sql = "SELECT * FROM " + payments_table_name + " WHERE acked_by_wallet = FALSE AND orphan = FALSE"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql)
    mysql_busy = False
    return poolCursor.fetchall()

def get_unconfirmed_blocks():
    global mysql_busy

    sql = "SELECT * FROM " + payments_table_name + " WHERE acked_by_wallet = TRUE AND confirmed = FALSE AND orphan = FALSE"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql)
    mysql_busy = False
    return poolCursor.fetchall()

def get_unpaid_payments():
    global mysql_busy

    sql = "SELECT * FROM " + payments_table_name + " WHERE paid = FALSE AND acked_by_wallet = TRUE AND confirmed = TRUE AND orphan = FALSE"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql)
    mysql_busy = False
    return poolCursor.fetchall()

def is_block_in_db_already(block):
    global mysql_busy

    sql = "SELECT * FROM " + payments_table_name + " WHERE reward_block = %s"
    while mysql_busy == True:
        pass
    mysql_busy = True
    poolCursor.execute(sql, (block,))
    mysql_busy = False
    result = poolCursor.fetchall()
    if len(result):
        return True
    else:
        return False
