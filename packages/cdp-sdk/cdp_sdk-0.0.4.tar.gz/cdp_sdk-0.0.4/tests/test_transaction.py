import pytest

from cdp.client.models.transaction import Transaction as TransactionModel
from cdp.transaction import Transaction


def test_transaction_initialization(transaction_factory):
    """Test transaction initialization."""
    transaction = transaction_factory()

    assert isinstance(transaction, Transaction)
    assert isinstance(transaction._model, TransactionModel)
    assert transaction._raw is None
    assert transaction._signature == "0xsignedpayload"


def test_transaction_initialization_invalid_model():
    """Test transaction initialization with an invalid model."""
    with pytest.raises(TypeError, match="model must be of type TransactionModel"):
        Transaction("invalid_model")


def test_unsigned_payload(transaction_factory):
    """Test unsigned payload."""
    transaction = transaction_factory()

    assert transaction.unsigned_payload == "0xunsignedpayload"


def test_signed_payload(transaction_factory):
    """Test signed payload."""
    transaction = transaction_factory()

    assert transaction.signed_payload == "0xsignedpayload"


def test_transaction_hash(transaction_factory):
    """Test transaction hash."""
    transaction = transaction_factory()

    assert transaction.transaction_hash == "0xtransactionhash"


@pytest.mark.parametrize(
    "status, expected_status",
    [
        ("pending", Transaction.Status.PENDING),
        ("signed", Transaction.Status.SIGNED),
        ("broadcast", Transaction.Status.BROADCAST),
        ("complete", Transaction.Status.COMPLETE),
        ("failed", Transaction.Status.FAILED),
        ("unspecified", Transaction.Status.UNSPECIFIED),
    ],
)
def test_status(transaction_factory, status, expected_status):
    """Test transaction status."""
    transaction = transaction_factory()

    transaction._model.status = status
    assert transaction.status == expected_status


def test_from_address_id(transaction_factory):
    """Test from address ID."""
    transaction = transaction_factory()

    assert transaction.from_address_id == "0xaddressid"


def test_to_address_id(transaction_factory):
    """Test to address ID."""
    transaction = transaction_factory()

    assert transaction.to_address_id == "0xdestination"


def test_terminal_state(transaction_factory):
    """Test terminal state."""
    unsigned_transaction = transaction_factory("pending")
    transaction = transaction_factory()

    assert not unsigned_transaction.terminal_state
    assert transaction.terminal_state


def test_block_hash(transaction_factory):
    """Test block hash."""
    transaction = transaction_factory()

    assert transaction.block_hash == "0xblockhash"


def test_block_height(transaction_factory):
    """Test block height."""
    transaction = transaction_factory()

    assert transaction.block_height == "123456"


def test_transaction_link(transaction_factory):
    """Test transaction link."""
    transaction = transaction_factory()

    assert transaction.transaction_link == "https://sepolia.basescan.org/tx/0xtransactionlink"


def test_signed(transaction_factory):
    """Test signed."""
    unsigned_transaction = transaction_factory("pending")
    transaction = transaction_factory()

    assert not unsigned_transaction.signed
    assert transaction.signed


def test_signature(transaction_factory):
    """Test signature."""
    transaction = transaction_factory()

    assert transaction.signature == "0xsignedpayload"


def test_signature_not_signed(transaction_factory):
    """Test signature not signed."""
    unsigned_transaction = transaction_factory("pending")

    with pytest.raises(ValueError, match="Transaction is not signed"):
        unsigned_transaction.signature  # noqa: B018


def test_str_representation(transaction_factory):
    """Test string representation."""
    transaction = transaction_factory()

    expected_str = "Transaction: (transaction_hash: 0xtransactionhash, status: complete)"
    assert str(transaction) == expected_str


def test_repr(transaction_factory):
    """Test repr."""
    transaction = transaction_factory()

    expected_repr = "Transaction: (transaction_hash: 0xtransactionhash, status: complete)"
    assert repr(transaction) == expected_repr
