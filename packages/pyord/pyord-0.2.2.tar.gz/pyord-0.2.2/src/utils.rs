use bitcoin::blockdata::transaction::Transaction;
use bitcoin::consensus::Decodable;
use bitcoin::consensus::encode::serialize_hex;
use hex;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

pub(crate) fn hex_to_bitcoin_tx(hex_tx: &str) -> PyResult<Transaction> {
    let decoded = hex::decode(hex_tx);
    let decoded = match decoded {
        Ok(d) => d,
        Err(e) => return Err(PyValueError::new_err(format!("Error decoding hex: {}", e))),
    };
    match Decodable::consensus_decode(&mut decoded.as_slice()) {
        Ok(tx) => Ok(tx),
        Err(e) => Err(
            PyValueError::new_err(
                format!(
                    "Error decoding transaction: {}",
                    e
                )
            )
        ),
    }
}

#[allow(unused)]
pub(crate) fn bitcoin_tx_to_hex(tx: &Transaction) -> String {
    serialize_hex(tx)
}

#[cfg(test)]
mod test {
    use super::*;

    const SOME_TX: &str = "0100000001a15d57094aa7a21a28cb20b59aab8fc7d1149a3bdbcddba9c622e4f5f6a99ece010000006c493046022100f93bb0e7d8db7bd46e40132d1f8242026e045f03a0efe71bbb8e3f475e970d790221009337cd7f1f929f00cc6ff01f03729b069a7c21b59b1736ddfee5db5946c5da8c0121033b9b137ee87d5a812d6f506efdd37f0affa7ffc310711c06c7f3e097c9447c52ffffffff0100e1f505000000001976a9140389035a9225b3839e2bbf32d826a1e222031fd888ac00000000";

    #[test]
    fn round_trip() {
        let tx = hex_to_bitcoin_tx(SOME_TX)?;
        println!("{:?}", tx);
        assert_eq!(tx.version, 1);
        assert_eq!(tx.input.len(), 1);
        assert_eq!(tx.output.len(), 1);
        let s = bitcoin_tx_to_hex(&tx);
        assert_eq!(s, SOME_TX);
    }
}