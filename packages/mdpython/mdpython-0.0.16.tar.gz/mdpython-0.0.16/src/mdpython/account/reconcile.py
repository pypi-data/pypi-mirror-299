import pandas as pd
from typing import List, Union


class Payment:
    def __init__(self, dt, amt):
        self.dt = dt
        self.amt = amt
        self.resolved_amt = 0
        self.unresolved_amt = amt
        self.bill_ar = []
        self.status = ''
        self.comment = ''

    def get_status(self):
        if self.resolved_amt == 0:
            self.status = "Unresolved"
        elif self.unresolved_amt == 0:
            self.status = "Resolved"
        else:
            self.status = "Partially Resolved"
        return self.status

    def get_comment(self):
        if not self.status:
            self.get_status()
        if self.status == "Unresolved":
            self.comment = ''
            return
        if len(self.bill_ar) == 1:
            b = self.bill_ar[0]
            self.comment = f"Paid {b['paid_amt']} for bill dated " + \
                           f"{b['obj'].dt.strftime('%d-%m-%Y')}"
        else:
            self.comment = f"Paid for {len(self.bill_ar)} bills - "
            for b in self.bill_ar:
                self.comment += f"Paid {b['paid_amt']} for bill dated " + \
                                f"{b['obj'].dt.strftime('%d-%m-%Y')} "

    def get_row(self):
        self.get_status()
        self.get_comment()
        return [self.dt, self.amt, self.status, self.comment]


class Bill:
    def __init__(self, dt, amt):
        self.dt = dt
        self.amt = amt
        self.paid_amt = 0
        self.unpaid_amt = amt
        self.discount = 0
        self.pymt_ar = []
        self.status = ''
        self.comment = ''

    def get_status(self):
        if self.paid_amt == 0:
            self.status = "Unpaid"
        elif self.unpaid_amt == 0 and self.discount == 0:
            self.status = "Paid"
        elif self.unpaid_amt == 0 and self.discount > 0:
            self.status = "Discounted Paid"
        else:
            self.status = "Partially Paid"
        return self.status

    def check_exact_match(self, amt):
        return self.amt == amt

    def check_disc_match(self, amt, disc_ar):
        for disc in disc_ar:
            disc_amt = self.amt * ((100 - disc) / 100)
            if amt - 1 <= disc_amt <= amt + 1:
                return {"match": True, "disc": disc, "round_amt": amt}
        return {"match": False}

    def provide_discount_and_settle(self, disc, round_amt, pymt):
        self.unpaid_amt = round_amt
        self.discount = disc
        self.settle(pymt)

    def settle(self, pymt: Payment):
        if pymt.unresolved_amt == 0 or self.unpaid_amt == 0:
            return
        if pymt.unresolved_amt >= self.unpaid_amt:
            amt_used = self.unpaid_amt
        else:
            amt_used = pymt.unresolved_amt
        self.paid_amt += amt_used
        self.unpaid_amt -= amt_used
        pymt.resolved_amt += amt_used
        pymt.unresolved_amt -= amt_used
        self.pymt_ar.append({"obj": pymt, "paid_amt": amt_used})
        pymt.bill_ar.append({"obj": self, "paid_amt": amt_used})

    def get_comment(self):
        if not self.status:
            self.get_status()
        if self.status == "Unpaid":
            self.comment = ''
            return
        if self.discount > 0:
            p = self.pymt_ar[0]
            self.comment = f"Paid {p['paid_amt']} on " + \
                           f"{p['obj'].dt.strftime('%d-%m-%Y')} with " + \
                           f"discount of {self.discount} %"
            return
        if len(self.pymt_ar) == 1:
            p = self.pymt_ar[0]
            self.comment = f"Paid {p['paid_amt']} on " + \
                           f"{p['obj'].dt.strftime('%d-%m-%Y')}"
        else:
            self.comment = f"Paid in {len(self.pymt_ar)} installments - "
            for p in self.pymt_ar:
                self.comment += f"Paid {p['paid_amt']} on " + \
                                f"{p['obj'].dt.strftime('%d-%m-%Y')} "

    def get_row(self):
        self.get_status()
        self.get_comment()
        return [self.dt, self.amt, self.status, self.comment]


class ReconcilePayment:
    def __init__(self, bill_ar: List[Bill], pymt_ar: List[Payment],
                 disc_ar: List[Union[int, float]]):
        self.bill_dtl_df: pd.DataFrame = pd.DataFrame()
        self.pymt_dtl_df: pd.DataFrame = pd.DataFrame()
        self.bill_ar = bill_ar
        self.pymt_ar = pymt_ar
        self.disc_ar = disc_ar

    def get_unpaid_bills_on_or_before(self, dt):
        return [x for x in self.bill_ar if x.dt <= dt and x.unpaid_amt > 0]

    def get_unpaid_bills(self):
        return [x for x in self.bill_ar if x.unpaid_amt > 0]

    def get_unresolved_payments(self):
        return [x for x in self.pymt_ar if x.unresolved_amt > 0]

    def get_unresolved_payments_on_or_after(self, dt):
        return [x for x in self.pymt_ar if x.unresolved_amt > 0 and x.dt >= dt]

    def match_exact_values(self):
        for pymt in self.get_unresolved_payments():
            for bill in self.get_unpaid_bills_on_or_before(pymt.dt):
                if bill.check_exact_match(pymt.amt):
                    bill.settle(pymt)

    def distribute_payment(self):
        for pymt in self.get_unresolved_payments():
            for bill in self.get_unpaid_bills_on_or_before(pymt.dt):
                bill.settle(pymt)
                if pymt.unresolved_amt == 0:
                    break

    def match_discounted_values(self):
        for pymt in self.get_unresolved_payments():
            for bill in self.get_unpaid_bills_on_or_before(pymt.dt):
                disc_mtch = bill.check_disc_match(pymt.amt, self.disc_ar)
                if disc_mtch["match"]:
                    bill.provide_discount_and_settle(disc_mtch["disc"],
                                                     disc_mtch["round_amt"],
                                                     pymt)

    def match_combined_payments(self):
        # One bill being paid in more than 1 payment
        for bill in self.get_unpaid_bills():
            pymt_ar = self.get_unresolved_payments_on_or_after(bill.dt)
            mtch = find_combinations_with_target_sum(pymt_ar, bill.unpaid_amt,
                                                     "unresolved_amt")
            if mtch:
                for pymt in mtch[0]:
                    bill.settle(pymt)

        # One payment being done for more than 1 bills
        for pymt in self.get_unresolved_payments():
            bill_ar = self.get_unpaid_bills_on_or_before(pymt.dt)
            mtch = find_combinations_with_target_sum(bill_ar,
                                                     pymt.unresolved_amt,
                                                     "unpaid_amt")
            if mtch:
                for bill in mtch[0]:
                    bill.settle(pymt)

    def reconcile(self):
        self.match_exact_values()
        self.match_discounted_values()
        self.match_combined_payments()
        self.distribute_payment()
        self.bill_dtl_df = pd.DataFrame([x.get_row() for x in self.bill_ar],
                                        columns=[
                                            "Bill Date", "Bill Amount",
                                            "Status", "Comment"])
        self.pymt_dtl_df = pd.DataFrame([x.get_row() for x in self.pymt_ar],
                                        columns=[
                                            "Payment Date", "Payment Amount",
                                            "Status", "Comment"])

    def to_excel(self, out_fl):
        self.bill_dtl_df.to_excel(out_fl, startcol=1, index=False)
        with pd.ExcelWriter(out_fl, mode="a", if_sheet_exists='overlay') as f:
            self.pymt_dtl_df.to_excel(f, startcol=6, index=False)


def find_combinations_with_target_sum(amt_obj_ar, target_amt, pmt_attrib_nm):
    result = []

    def backtrack(start, current_combination, current_sum):
        if current_sum == target_amt:
            result.append(list(current_combination))
            return
        if current_sum > target_amt:
            return

        for i in range(start, len(amt_obj_ar)):
            current_combination.append(amt_obj_ar[i])
            backtrack(i + 1, current_combination,
                      current_sum + getattr(amt_obj_ar[i], pmt_attrib_nm))
            current_combination.pop()

    backtrack(0, [], 0)
    return result


def reconcile_payment(bill_df: pd.DataFrame, pymt_df: pd.DataFrame,
                      bill_dt_col: str, bill_amt_col: str, pymt_dt_col: str,
                      pymt_amt_col: str,
                      disc_ar: List[Union[int, float]]) -> ReconcilePayment:
    bill_ar = [Bill(x[0], x[1]) for x in sorted(
        bill_df[[bill_dt_col, bill_amt_col]].values.tolist())]
    pymt_ar = [Payment(x[0], x[1]) for x in sorted(
        pymt_df[[pymt_dt_col, pymt_amt_col]].values.tolist())]
    disc_ar = disc_ar
    recon = ReconcilePayment(bill_ar, pymt_ar, disc_ar)
    recon.reconcile()
    return recon
