class TestExchange:
    def test_exchange(self, exchange, u1, u2, u3):
        exchange.register_user(u1)
        exchange.register_user(u2)
        exchange.register_user(u3)

        u1.place_order(exchange, "Stock A", "limit", "buy", 50, 10)
        u1.place_order(exchange, "Stock A", "limit", "sell", 50, 20)

        assert exchange.order_books["Stock A"].last_price is None
        assert u1.realised_pnl == 0
        assert len(u1.positions) == 0

        u2.place_order(exchange, "Stock A", "limit", "sell", 50, 10)
        assert len(u1.positions) == 1
        assert u1.realised_pnl == 0
        assert u2.realised_pnl == 0

        u3.place_order(exchange, "Stock A", "limit", "buy", 25, 20)
        assert len(u1.positions) == 1
        assert len(u3.positions) == 1
        assert u1.realised_pnl == 250
        assert u3.realised_pnl == 0

        u3.place_order(exchange, "Stock A", "limit", "buy", 25, 20)
        assert len(u1.positions) == 0
        assert len(u3.positions) == 1
        assert u1.realised_pnl == 500
        assert u3.realised_pnl == 0
    
        u3.place_order(exchange, "Stock A", "limit", "sell", 50, 10)
        assert len(u1.positions) == 0
        assert len(u3.positions) == 1
        assert u1.realised_pnl == 500
        assert u3.realised_pnl == 0

        u2.place_order(exchange, "Stock A", "limit", "buy", 50, 10)
        assert len(u1.positions) == 0
        assert len(u3.positions) == 0
        assert u1.realised_pnl == 500
        assert u3.realised_pnl == -500
        
