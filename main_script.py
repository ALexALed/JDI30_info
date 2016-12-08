from data_writer import CompanyDataWriter


with CompanyDataWriter() as writer:
    writer.create_table()
