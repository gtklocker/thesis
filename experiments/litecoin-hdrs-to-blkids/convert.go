package main

import (
	"os"
	"io"
	"golang.org/x/crypto/scrypt"
	"gopkg.in/cheggaaa/pb.v1"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func hdrToId(hdr []byte) ([]byte, error) {
	return scrypt.Key(hdr, hdr, 1024, 1, 1, 32)
}

func main() {
	HDR_SIZE_BYTES := 80

	hdrFile, err := os.Open("Litecoin-Mainnet.bin")
	check(err)

	outFile, err := os.Create("Litecoin-Mainnet-ids.bin")
	check(err)

	hdr := make([]byte, HDR_SIZE_BYTES)

	stat, err := hdrFile.Stat()
	check(err)

	totalHdrs := stat.Size() / int64(HDR_SIZE_BYTES)
	bar := pb.StartNew(int(totalHdrs))

	for {
		n1, err := hdrFile.Read(hdr)
		if err == io.EOF || n1 < HDR_SIZE_BYTES {
			break
		} else {
			check(err)
		}

		id, err := hdrToId(hdr)
		check(err)

		n2, err := outFile.Write(id)
		check(err)
		_ = n2

		bar.Increment()
	}
}
