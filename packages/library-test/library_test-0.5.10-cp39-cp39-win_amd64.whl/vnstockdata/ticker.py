from vnstockdata.config.ensure_logged_in import ensure_logged_in
from vnstockdata.stock.price import get_price
import pandas as pd 
from datetime import datetime 
class Ticker:
    def __init__(self,ticker) -> None:
        """
        Khởi tạo đối tượng Ticker với mã cổ phiếu cụ thể.

        Args:
            ticker (str): Mã cổ phiếu (ví dụ: "HPG").
        """
        self.ticker=ticker
    @ensure_logged_in
    def history(self,fromDate,toDate):
        """
        Trả về dữ liệu lịch sử giao dịch của mã cổ phiếu trong khoảng thời gian cụ thể.

        Args:
            fromDate (str): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'.
            toDate (str): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: Dữ liệu giao dịch của mã cổ phiếu, bao gồm các cột như giá mở cửa, giá đóng cửa, khối lượng giao dịch, v.v.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD').
            Exception: Nếu có lỗi xảy ra khi kết nối API hoặc token hết hạn.

        Example:
            >>> ticker = Ticker("HPG")
            >>> df = ticker.history("2024-01-01", "2024-09-30")
            >>> print(df.head())
        """
        data=get_price(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate
        )
        return data