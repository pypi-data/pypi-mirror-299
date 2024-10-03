from vnstockdata.config.ensure_logged_in import ensure_logged_in
from vnstockdata.stock.price import get_price
import pandas as pd
from datetime import datetime

class Ticker:
    """
    Lớp Ticker đại diện cho một mã cổ phiếu và cung cấp phương thức để lấy dữ liệu liên quan đến mã cổ phiếu.

    Attributes:
        ticker (str): Mã cổ phiếu, ví dụ như "HPG".
    """

    def __init__(self, ticker: str) -> None:
        """
        Khởi tạo đối tượng Ticker với mã cổ phiếu cụ thể.

        Args:
            ticker (str): Mã cổ phiếu (ví dụ: "HPG").
        """
        self.ticker = ticker

    @ensure_logged_in
    def history(self, fromDate: str, toDate: str) -> pd.DataFrame:
        """
        Trả về dữ liệu lịch sử giao dịch của mã cổ phiếu trong khoảng thời gian cụ thể.

        Phương thức này yêu cầu người dùng đã đăng nhập và lấy dữ liệu giao dịch của mã cổ phiếu 
        từ ngày `fromDate` đến ngày `toDate`. Dữ liệu bao gồm giá mở cửa, giá đóng cửa, khối lượng giao dịch, và các thông tin khác.

        Args:
            fromDate (str): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'.
            toDate (str): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: Dữ liệu giao dịch của mã cổ phiếu, bao gồm các cột như giá mở cửa, giá đóng cửa, khối lượng giao dịch, v.v.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD').
            Exception: Nếu có lỗi xảy ra khi kết nối API hoặc token hết hạn.

        Example:
            >>> import vnstockdata as vn
            >>> hpg = vn.Ticker("HPG")
            >>> df = hpg.history("2024-01-01", "2024-09-30")
            >>> print(df.head())
        """
        data = get_price(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate
        )
        return data
